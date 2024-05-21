from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from store.models import *
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def track_delivery(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        shipping = Shipping.objects.get(order=order)
    except (Order.DoesNotExist, Shipping.DoesNotExist):
        # handle the case where either the Cart or Shipping object does not exist
        return HttpResponseNotFound("Awaiting shipment")
    
    context = {
        'order': order,
        'shipping': shipping
    }
    
    return render(request, 'shipping/track_shipping.html', context)

class ServiceDeliveredListView(ListView):
    model = Shipping
    template_name = 'service_provider/pages/Service_delivered_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.SERVICE_PROVIDER:
            return Shipping.objects.filter(status__in=[Shipping.Status.DELIVERED])
        return super().get_queryset()

class DriverShippingListView(ListView):
    model = Shipping
    template_name = 'driver/pages/driver_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DRIVER:
            return Shipping.objects.filter(driver=user, status=Shipping.Status.PENDING)
        return super().get_queryset()


class OutForDeliveryListView(ListView):
    model = Shipping
    template_name = 'driver/pages/driver_out_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DRIVER:
            return Shipping.objects.filter(driver=user, status__in=[Shipping.Status.OUT_FOR_DELIVERY])
        return super().get_queryset()

class DeliveredListView(ListView):
    model = Shipping
    template_name = 'driver/pages/driver_delivered_shipping_list.html'
    context_object_name = 'shipping_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == user.UserTypes.DRIVER:
            queryset = Shipping.objects.filter(driver=user, status=Shipping.Status.DELIVERED)
            return queryset
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UpdateShippingStatusView(View):
    def post(self, request, pk):
        shipping = Shipping.objects.get(pk=pk)
        if shipping.driver != request.user:
            return redirect('shipping:driver-shipping-list')

        status = request.POST.get('status')
        if status == Shipping.Status.OUT_FOR_DELIVERY:
            shipping.status = Shipping.Status.OUT_FOR_DELIVERY
        elif status == Shipping.Status.DELIVERED:
            shipping.status = Shipping.Status.DELIVERED
        shipping.save()

        return redirect('shipping:driver-shipping-list')

@login_required
def update_shipping_status(request, pk):
    shipping = get_object_or_404(Shipping, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == Shipping.Status.DELIVERED:
            shipping.status = Shipping.Status.DELIVERED
        elif status == Shipping.Status.COMPLETE:
            shipping.status = Shipping.Status.COMPLETE
        shipping.save()

        return redirect('store:customer-order-list')
    
    return redirect('store:customer-order-list')

@login_required
def reject_shipping(request, pk):
    shipping = get_object_or_404(Shipping, pk=pk)

    if request.method == 'POST':
        rejection_message = request.POST.get('rejection_message')
        shipping.status = Shipping.Status.REJECTED
        shipping.rejection_message = rejection_message
        shipping.save()

        return redirect('store:customer-order-list')
    
    return redirect('store:customer-order-list')
