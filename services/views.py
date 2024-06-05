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
from django.urls import reverse_lazy
from xhtml2pdf import pisa
from django.urls import reverse
from django.views.generic import ListView
from finance.forms import BookingPaymentForm
from finance.models import *
from .forms import *
from .models import * 

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
        form.instance.tools_required = form.instance.service.tools_required  # Autofill tools_required
        return super().form_valid(form)

    def get_success_url(self):
        booking_id = self.object.id  # Retrieve the ID of the newly created ServiceBooking object
        return reverse('services:booking-checkout', kwargs={'booking_id': booking_id})

@login_required
def booking_checkout(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=int(booking_id), user=request.user)
    
    if request.method == 'POST':
        form = BookingPaymentForm(data=request.POST)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            payment_status = 'pending'  # Set the payment_status to "pending"
            booking_payment, created = BooKingPayment.objects.get_or_create(booking=booking, user=request.user)
            booking_payment.location = form.cleaned_data['location']  # Get location from the form
            booking_payment.address = form.cleaned_data['address']  # Get address from the form
            booking_payment.transaction_id = transaction_id
            booking_payment.payment_status = payment_status
            booking_payment.save()

            messages.success(request, 'Payment successful. Thank you!')
            return redirect('services:view-services')
    else:
        # Initialize the form with initial data including the location from the booking
        initial_data = {'location': booking.location}
        form = BookingPaymentForm(initial=initial_data)

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


@login_required
def track_progress(request, booking_id):
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    assignment = booking.installer_assignment if hasattr(booking, 'installer_assignment') else None

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            booking.service_delivered = True
            booking.customer_approval = form.cleaned_data['customer_approval']
            booking.customer_feedback = form.cleaned_data['customer_feedback']
            booking.save()
            messages.success(request, 'Your feedback has been submitted.')
            return redirect('services:track_progress', booking_id=booking.id)
    else:
        form = FeedbackForm()

    context = {
        'booking': booking,
        'assignment': assignment,
        'form': form,
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

def assign_installer(request):
    if request.method == 'POST':
        installer_id = request.POST.get('installer_id')
        booking_id = request.POST.get('booking_id')
        print(f"Installer ID: {installer_id}, Booking ID: {booking_id}")  # Add this line for debugging
        booking = get_object_or_404(ServiceBooking, pk=booking_id)
        installer = get_object_or_404(User, pk=installer_id, user_type=User.UserTypes.INSTALLER)

        # Check if the operator is already assigned to the booking
        if InstallerAssignment.objects.filter(booking=booking, installer=installer).exists():
            return redirect('services:assigned-installer')  # Replace with the desired URL or view name for the error page

        assignment = InstallerAssignment(booking=booking, installer=installer)
        assignment.save()

        return redirect('services:assigned-installer')  # Replace 'operator_assigned' with your desired success URL

    # Modify the filter condition to include the booking_payment__payment_status
    booking_list = ServiceBooking.objects.filter(
        installer_assignment__isnull=True,  # Filter out bookings with an assigned operator
        bookingpayment__payment_status='approved'  # Filter by payment status 'approved'
    )

    installer = User.objects.filter(user_type=User.UserTypes.INSTALLER, is_active=True)

    context = {
        'booking_list': booking_list,
        'installer': installer,
    }

    return render(request, 'services/assign_installer.html', context)



def assigned_installer(request):

    # Modify the filter condition to include the booking_payment__payment_status
    booking_list = ServiceBooking.objects.filter(
        installer_assignment__isnull=False,  # Filter out bookings with an assigned installer
        bookingpayment__payment_status='approved'  # Filter by payment status 'approved'
    )

    installer = User.objects.filter(user_type=User.UserTypes.INSTALLER, is_active=True)

    context = {
        'booking_list': booking_list,
        'installer': installer,
    }

    return render(request, 'services/assign_installer.html', context)


# installer
@login_required
def installer_list(request):
    # Get the current logged-in user
    user = request.user

    # Check if the user is a machine installer
    if user.user_type == User.UserTypes.INSTALLER:
        # Modify the filter condition to include the booking_payment__payment_status
        booking_list = ServiceBooking.objects.filter(
            installer_assignment__installer=user,  # Filter bookings where the installer is the current user
            installer_assignment__status=InstallerAssignment.AssignmentStatus.ASSIGNED,  # Filter assignments with status 'assigned'
            bookingpayment__payment_status='approved'  # Filter by payment status 'approved'
        )

        installers = User.objects.filter(user_type=User.UserTypes.INSTALLER, is_active=True)

        context = {
            'booking_list': booking_list,
            'installers': installers,
        }

        return render(request, 'installer/pages/installer.html', context)

    # If the user is not a machine installer, you can handle this case accordingly.
    # For example, you can redirect them to an error page or another view.

    # Replace 'error_page' with the desired URL or view name for handling non-installer users
    return redirect('services:installer_list')

@login_required
def request_tools(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=booking_id, installer_assignment__installer=request.user)

    if request.method == 'POST':
        form = ToolRequestForm(request.POST)
        if form.is_valid():
            assignment = booking.installer_assignment
            assignment.tools_requested = True
            assignment.save()
            return redirect('services:installer_list')
    else:
        form = ToolRequestForm()

    return render(request, 'installer/pages/request_tools.html', {'form': form, 'booking': booking, 'tools_required': booking.tools_required})

@login_required
def installer_completed_list(request):
    # Get the current logged-in user
    user = request.user

    # Check if the user is a machine installer
    if user.user_type == User.UserTypes.INSTALLER:
        # Modify the filter condition to include the booking_payment__payment_status
        booking_list = ServiceBooking.objects.filter(
            installer_assignment__installer=user,  # Filter bookings where the installer is the current user
            installer_assignment__status=InstallerAssignment.AssignmentStatus.COMPLETED,  # Filter assignments with status 'completed'
            bookingpayment__payment_status='approved'  # Filter by payment status 'approved'
        )

        installers = User.objects.filter(user_type=User.UserTypes.INSTALLER, is_active=True)

        context = {
            'booking_list': booking_list,
            'installers': installers,
        }

        return render(request, 'installer/pages/installer.html', context)

    # If the user is not a machine installer, you can handle this case accordingly.
    # For example, you can redirect them to an error page or another view.

    # Replace 'error_page' with the desired URL or view name for handling non-installer users
    return redirect('services:installer_list')


@login_required
def mark_booking_complete(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=booking_id, installer_assignment__installer=request.user)
    assignment = booking.installer_assignment

    if assignment.tools_provided:
        assignment.status = InstallerAssignment.AssignmentStatus.COMPLETED
        assignment.save()
        return redirect('services:installer_list')

    return HttpResponse("Tools have not been provided yet.", status=403)


@login_required
def manage_tool_requests(request):
    if request.user.user_type != User.UserTypes.SERVICE_PROVIDER:
        return HttpResponse("Unauthorized", status=403)

    tool_requests = InstallerAssignment.objects.filter(tools_requested=True, tools_provided=False)

    context = {
        'tool_requests': tool_requests,
    }

    return render(request, 'service_provider/pages/manage_tool_requests.html', context)

@login_required
def provide_tools(request, assignment_id):
    if request.user.user_type != User.UserTypes.SERVICE_PROVIDER:
        return HttpResponse("Unauthorized", status=403)

    assignment = get_object_or_404(InstallerAssignment, id=assignment_id)

    if request.method == 'POST':
        form = ToolAssignmentForm(request.POST)
        if form.is_valid():
            assignment.tools_provided = True
            assignment.save()
            return redirect('services:manage_tool_requests')
    else:
        form = ToolAssignmentForm()

    return render(request, 'service_provider/pages/provide_tools.html', {'form': form, 'assignment': assignment, 'tools_required': assignment.booking.tools_required})


@login_required
def provided_tools(request):
    if request.user.user_type != User.UserTypes.SERVICE_PROVIDER:
        return HttpResponse("Unauthorized", status=403)

    # Fetch all assignments where tools have been provided
    provided_tools_list = InstallerAssignment.objects.filter(tools_provided=True).select_related('booking__service', 'installer')

    context = {
        'provided_tools_list': provided_tools_list,
    }

    return render(request, 'service_provider/pages/provided_tools.html', context)


def service_bookings(request):
    bookings = ServiceBooking.objects.all()
    return render(request, 'service_provider/pages/service_bookings.html', {'bookings': bookings})