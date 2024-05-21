from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import *
from .utils import calculate_delivery_fee
from decimal import Decimal, InvalidOperation
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
from moneyed import Money 
from django.contrib.auth.decorators import login_required 
# reports
from django.db.models import F, Sum
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from finance.utils import calculate_delivery_fee


@login_required
def checkout(request):
    try:
        order = Order.objects.filter(user=request.user, is_completed=False).latest('id')
    except Order.DoesNotExist:
        messages.error(request, 'Your order is empty.')
        return redirect('store:view-products')

    order_items = order.orderitem_set.all()
    
    # Check for any items with None as price
    for item in order_items:
        if item.product.price is None:
            messages.error(request, f"Item {item.product.name} has no price set.")
            return redirect('store:view_cart')
    
    # Calculate order total
    try:
        order_total = sum(item.subtotal().amount for item in order_items if item.product.price is not None)
        order_total = Money(Decimal(order_total), 'KES')
    except (InvalidOperation, TypeError) as e:
        messages.error(request, 'There was an error calculating your order total.')
        return redirect('store:view_cart')

    delivery_fee = calculate_delivery_fee(order_total)

    # Ensure delivery_fee is also a Money object
    total_with_delivery = order_total + delivery_fee

    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    address_form_initial_data = {
        'town': customer_profile.town,
        'phone_number': getattr(request.user, 'phone_number', ''),
        'county': customer_profile.county
    }

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST, instance=customer_profile)

        if payment_form.is_valid() and address_form.is_valid():
            transaction_id = payment_form.cleaned_data['transaction_id']
            address = address_form.save()

            customer_profile.phone_number = address.phone_number
            customer_profile.town = address.town
            customer_profile.county = address.county
            customer_profile.save()

            try:
                payment = OrderPayment.objects.get(order=order)
                payment.transaction_id = transaction_id
                payment.payment_status = 'pending'
                payment.save()
            except OrderPayment.DoesNotExist:
                payment = OrderPayment.objects.create(
                    order=order,
                    transaction_id=transaction_id,
                    payment_status='pending',
                    town=address.town,
                    county=address.county,
                    phone_number=address.phone_number,
                )

            for item in order_items:
                product = item.product
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    product.save()
                else:
                    messages.error(request, f"{product.name} is out of stock.")
                    return redirect('store:view_cart')

            order.is_completed = True
            order.save()

            messages.success(request, 'Payment was successful!')
            return redirect('store:view_cart')
    else:
        address_form = AddressForm(instance=customer_profile, initial=address_form_initial_data)
        payment_form = PaymentForm()

    context = {
        'payment_form': payment_form,
        'address_form': address_form,
        'order_items': order_items,
        'order_total': order_total,
        'delivery_fee': delivery_fee,
        'total_with_delivery': total_with_delivery
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

    # Convert amounts to Money and calculate total_with_delivery
    for item in sales_data:
        order_total = Money(Decimal(item['order_total_amount']), 'KES')
        delivery_fee = calculate_delivery_fee(order_total)
        item['total_with_delivery'] = order_total + delivery_fee

    # Calculate the total amount of money made
    total_amount = sum(item['total_with_delivery'] for item in sales_data)

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
            item['total_with_delivery'],  # Display the order total amount in the table
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



