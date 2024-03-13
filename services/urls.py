from services import views

from django.urls import path

from .views import *

app_name = "services"

urlpatterns = [
    path('view-services/',ServiceView.as_view(), name='view-services'),
    path('services/book/<int:service_id>/', BookServiceView.as_view(), name='book_service'),
    path('booked-services/', BookedServicesListView.as_view(), name='booked-services'),
    path('booking-checkout/<int:booking_id>/', booking_checkout, name='booking-checkout'),
    path('pending-booked-services/', BookingPaymentListView.as_view(), name='pending-booked-services'),
    path('approved-booked-services/', BookingPaymentApprovedListView.as_view(), name='approved-booked-services'),
    path('approve-booking-payment/<str:transaction_id>/', approve_booking_payment, name='approve-booking-payment'),
    
    
    #invoice
    path('service-booking/<int:booking_id>/pdf/', service_booking_pdf, name='service_booking_pdf'),
    path('track-progress/<int:booking_id>/', track_progress, name='track_progress'),
]
 