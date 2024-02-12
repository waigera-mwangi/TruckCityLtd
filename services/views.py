from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.urls import reverse
from services.models import * 

# view services
class ServiceView(View):
    def get(self, request):
        services =  Service.objects.all()
        context = {'services': services}
        return render(request, 'customer/pages/service.html', context)
    
    # book service
class BookServiceView(View):
    template_name = 'services/book_service.html'

    @method_decorator(login_required)
    def get(self, request, service_id):
        service = Service.objects.get(pk=service_id)
        return render(request, self.template_name, {'service': service})

    @method_decorator(login_required)
    def post(self, request, service_id):
        service = Service.objects.get(pk=service_id)
        user = request.user

        # Check if the user has already booked this service
        if ServiceBooking.objects.filter(user=user, service=service).exists():
            messages.warning(request, 'You have already booked this service.')
            return redirect('services:view-services')

        # Create a new booking
        booking = ServiceBooking.objects.create(user=user, service=service)

        messages.success(request, f'You have successfully booked {service.name}.')
        return redirect('services:view-services')

    
    