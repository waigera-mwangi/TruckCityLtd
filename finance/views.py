from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import *
from store.models import Order, OrderItem
from .models import OrderPayment
from django.http import HttpResponse
from supply.models import SupplyTender
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from accounts.models import Profile, CustomerProfile
from io import BytesIO
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa

# reports
from django.db.models import F, Sum
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def checkout(request):
    user = User.objects.get(pk=1)
    order_items = OrderItem.objects.all()

    # Get the latest pending order for the logged-in user
    try:
        order = Order.objects.filter(user=request.user, is_completed=False).latest('id')
    except Order.DoesNotExist:
        messages.error(request, 'Your order is empty.')
        return redirect('store:view-products')

    order_items = order.orderitem_set.all()
    order_total = sum([item.subtotal() for item in order_items])

    # Create a  object for the user if it does not exist already
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    try:
        _profile = CustomerProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        _profile = CustomerProfile.objects.create(user=request.user)
    
    payment_form = PaymentForm(request.POST)
    address_form = AddressForm(request.POST, instance=_profile, initial={
        'town':_profile.town,
        'phone_number': request.user.phone_number if hasattr(request.user, 'phone_number') else '',
        'county':_profile.county
        # Add other fields you want to prepopulate from  profile
    })

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST, instance=_profile, initial={
        'town':_profile.town,
        'phone_number': request.user.phone_number if hasattr(request.user, 'phone_number') else '',
        'county':_profile.county,
        # Add other fields you want to prepopulate from  profile
    })
        if payment_form.is_valid() and address_form.is_valid():
            transaction_id = payment_form.cleaned_data['transaction_id']
            
            # Save user address
            address = address_form.save()

            # Update the phone_number in the Profile
            _profile.phone_number = address.phone_number
            _profile.town = address.town
            _profile.county = address.county
            _profile.save()

            # Check if a payment record already exists for the current order
            try:
                payment = OrderPayment.objects.get(order=order)
                payment.transaction_id = transaction_id
                payment.payment_status = 'Pending'
                payment.save()
            except OrderPayment.DoesNotExist:
                # enter data into payment model
                payment = OrderPayment.objects.create(
                    order=order,
                    transaction_id=transaction_id,
                    payment_status='pending',
                    town=address.town,
                    county=address.county,
                    phone_number=address.phone_number,
                    )
            
            # Update product quantity in stock
            for item in order_items:
                product = item.product
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    if product.quantity < 0: # check if the updated quantity is a positive integer
                        messages.error(request, f"{product.name} is out of stock.")
                        return redirect('store:view_cart')
                    product.save()
                else:
                    messages.error(request, f"{product.name} is out of stock.")
                    return redirect('store:view_cart')

            # Set the order as completed
            order.is_completed = True
            order.save()

            messages.success(request, 'Payment was successful!')
            return redirect('store:view_cart')
    else:
        address_form = AddressForm(instance=_profile, initial={
            'town': _profile.town,
            'phone_number': request.user.phone_number if hasattr(request.user, 'phone_number') else '',
            'county': _profile.county,
            # Add other fields you want to prepopulate from  profile
        })
        payment_form = PaymentForm()
       
    context = {
        'payment_form': payment_form,
        'address_form':address_form,
        'order_items': order_items,
        'order_total': order_total,
        
    }
    return render(request, 'customer/pages/checkout.html', context)


def receipt(request, tender_id):
    tender = get_object_or_404(SupplyTender, id=tender_id, tender_status='Complete')

    receipt_data = {
        'transaction_id': tender.id,
        'username': tender.user.get_full_name,
        'quantity': tender.quantity,
        'total_cost': tender.total(),
        'payment_status': tender.tender_status,
        'date_tender': tender.date,
        'product': tender.product.name,
        'price': tender.price,
    }

    # Render the receipt HTML template
    receipt_html = render_to_string('supplier/pages/supplier-receipt.html', receipt_data)

    # Create a file-like buffer to receive PDF data
    pdf_buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    pisa_status = pisa.CreatePDF(receipt_html, dest=pdf_buffer)

    # Return the receipt PDF as a downloadable response
    if pisa_status.err:
        return HttpResponse('An error occurred: %s' % pisa_status.err)
    else:
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=Receipt_{tender.id}.pdf'
        return response


# reports
def sales_report(request):
    # Fetch the data with additional details
    sales_data = OrderPayment.objects.values(
        'payment_status', 'order__user__username', 'payment_date', 'transaction_id'
    ).annotate(
        order_total_amount=Sum(F('order__orderitem__quantity') * F('order__orderitem__product__price')),
        total_sales=Sum('order__id')
    )

    # Calculate the total amount of money made
    total_amount = sum(item['order_total_amount'] for item in sales_data)

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add a title to the PDF
    title_style = getSampleStyleSheet()['Title']
    title = Paragraph("Order Reports", title_style)
    elements.append(title)

    # Create the table with the sales report data
    data = [['No.','User', 'Payment Status', 'Date', 'Transaction ID', 'Order Total Amount']]
    for index, item in enumerate(sales_data, start=1):
        data.append([
            index,
            item['order__user__username'],
            item['payment_status'].title(),
            item['payment_date'],
            item['transaction_id'],
            item['order_total_amount'],  # Display the order total amount in the table
        ])

    # Add the final row with the total amount
    data.append(['', '', '','', 'Total Amount:', total_amount])

    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#c0c0c0'),
                               ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), '#F0F0F0'),
                               ('GRID', (0, 0), (-1, -1), 1, '#888888')]))

    elements.append(table)

    # Build the PDF
    doc.build(elements)
    return response

