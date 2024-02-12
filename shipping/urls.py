from django.urls import path
from .views import *

app_name = 'shipping'


urlpatterns = [

	# path('select-pickup-station', UserPickUpStationCreateView.as_view(), name='select-pickup-station'),
	path('track_shipping/<str:order_id>/', track_delivery, name='track_shipping'),
    path('delivered-order/', ServiceDeliveredListView.as_view(), name='delivered-orders'),
    
    # driver
    path('driver/shipping-list', DriverShippingListView.as_view(), name='driver-shipping-list'),
    path('outfordelivery_shipping/', OutForDeliveryListView.as_view(), name='out-for-delivery'),
    path('delivered_shipping/', DeliveredListView.as_view(), name='delivered'),
    path('update_shipping/<str:pk>/', UpdateShippingStatusView.as_view(), name='update_shipping'),
    path('update_shipping_status/<str:pk>/', update_shipping_status, name='update_shipping_status'),
   

]