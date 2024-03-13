from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.template.loader import get_template 
from io import BytesIO
from django.http import HttpResponse

from xhtml2pdf import pisa
from django.urls import reverse
from django.views.generic import ListView
from finance.forms import BookingPaymentForm
from finance.models import *
from .forms import *
from services.models import * 

# view services
class ServiceView(View):
    def get(self, request):
        services =  Service.objects.all()
        context = {'services': services}
        return render(request, 'customer/pages/service.html', context)
    
    # book service
# class BookServiceView(View):
#     template_name = 'services/book_service.html'

#     @method_decorator(login_required)
#     def get(self, request, service_id):
#         service = Service.objects.get(pk=service_id)
#         return render(request, self.template_name, {'service': service})

#     @method_decorator(login_required)
#     def post(self, request, service_id):
#         service = Service.objects.get(pk=service_id)
#         user = request.user

#         # Check if the user has already booked this service
#         if ServiceBooking.objects.filter(user=user, service=service).exists():
#             messages.warning(request, 'You have already booked this service.')
#             return redirect('services:view-services')

#         # Create a new booking
#         booking = ServiceBooking.objects.create(user=user, service=service)

#         messages.success(request, f'You have successfully booked {service.name}.')
#         return redirect('services:view-services')

    
class BookServiceView(LoginRequiredMixin, CreateView):
    model = ServiceBooking
    form_class = BookingServiceForm
    template_name = 'services/book_service.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.service_id = self.kwargs['service_id']
        return super().form_valid(form)

    def get_success_url(self):
        booking_id = self.object.id  # Retrieve the ID of the newly created ServiceBooking object
        return reverse('services:booking-checkout', kwargs={'booking_id': booking_id})


@login_required
def booking_checkout(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=int(booking_id), user=request.user)
    payment = BooKingPayment.objects.filter(booking=booking).first()

    if request.method == 'POST':
        form = BookingPaymentForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            address = form.cleaned_data['address']
            transaction_id = form.cleaned_data['transaction_id']
            payment_status = 'pending'  # Set the payment_status to "pending"

            booking_payment, created = BooKingPayment.objects.get_or_create(booking=booking)
            booking_payment.location = location
            booking_payment.address = address
            booking_payment.transaction_id = transaction_id
            booking_payment.payment_status = payment_status
            booking_payment.save()

            messages.success(request, 'Payment successful. Thank you!')
            return redirect('services:view-services')
    else:
        form = BookingPaymentForm()

    return render(request, 'customer/pages/booking_checkout.html', {'booking': booking, 'form': form})


class BookedServicesListView(LoginRequiredMixin, ListView):
    template_name = 'customer/pages/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user
        bookings = ServiceBooking.objects.filter(user=user)
        
        for booking in bookings:
            booking_payment = BooKingPayment.objects.filter(booking=booking).first()
            if booking_payment:
                booking.booking_payment_status = booking_payment.payment_status
            else:
                booking.booking_payment_status = 'pending'  # Set a default payment status if payment not found
        
        return bookings



from django.db.models import Q


# service invoice
def service_booking_pdf(request, booking_id):
    # Get the ServiceBooking object or return a 404 error if not found
    booking = get_object_or_404(ServiceBooking, pk=booking_id)

    # Retrieve related data
    user = booking.user
    service = booking.service
    booking_date = booking.booking_date

    # Load template for receipt
    template = get_template('customer/pages/service-booking-receipt.html')
    context = {
        'booking': booking,
        'user': user,
        'service': service,
        'booking_date': booking_date,
    }
    html = template.render(context)

    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), buffer)

    if not pdf.err:
        # Get the value of the BytesIO buffer and write it to the response
        pdf_value = buffer.getvalue()
        buffer.close()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="service_booking_{booking_id}_receipt.pdf"'
        response.write(pdf_value)
        return response

    return HttpResponse('Error generating PDF!')


def track_progress(request, booking_id):
    # Get the ServiceBooking object or return a 404 error if not found
    
    booking = get_object_or_404(ServiceBooking, pk=booking_id)

    # Get the related MachineOperatorAssignment or return None if not found
    assignment = booking.operator_assignment if hasattr(booking, 'operator_assignment') else None

    context = {
        'booking': booking,
        'assignment': assignment,
    }

    return render(request, 'services/track_progress.html', context)
    

class BookingPaymentListView(ListView):
    template_name = 'finance_manager/pages/booking_payment_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Change the queryset to filter by payment_status being 'pending'
        bookings = ServiceBooking.objects.filter(bookingpayment__payment_status='pending')
        return bookings

class BookingPaymentApprovedListView(ListView):
    template_name = 'finance_manager/pages/approved_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Filter ServiceBooking instances based on the approval status of their associated BookingPayment
        bookings = ServiceBooking.objects.filter(bookingpayment__payment_status='approved')
        return bookings
    
    
def approve_booking_payment(request, transaction_id):
    booking_payment = get_object_or_404(BooKingPayment, transaction_id=transaction_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'approve':
            booking_payment.payment_status = 'approved'
            booking_payment.save()
            # Additional logic after approving the payment
        elif status == 'reject':
            booking_payment.payment_status = 'rejected'
            booking_payment.save()
            # Additional logic after rejecting the payment
        return redirect('services:approved-booked-services')

    context = {
        'payment': booking_payment,
    }
    return render(request, 'finance_manager/pages/booking_payment_list.html', context)

