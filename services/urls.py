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
    path('assign-installer/', assign_installer, name='assign-installer'),
    path('assigned-installer/', assigned_installer, name='assigned-installer'),
    path('installer-list/', installer_list, name='installer_list'),
    path('request-tools/<int:booking_id>/', views.request_tools, name='request_tools'),
    path('installer-completed-list/', installer_completed_list, name='installer_completed_list'),
    path('mark-complete/<int:booking_id>/', mark_booking_complete, name='mark-complete'),
    
    path('manage-tool-requests/', views.manage_tool_requests, name='manage_tool_requests'),
    path('provide-tools/<int:assignment_id>/', views.provide_tools, name='provide_tools'),
    path('provided-tools/', provided_tools, name='provided_tools'),
    
    #invoice
    path('service-booking/<int:booking_id>/pdf/', service_booking_pdf, name='service_booking_pdf'),
    path('track-progress/<int:booking_id>/', track_progress, name='track_progress'),
]
 