from django.urls import path
from . import views
from .views import *

app_name = 'finance'


urlpatterns = [
	path('checkout/', views.checkout, name='checkout'),
	path('supply-receipt/<int:tender_id>/', receipt, name='receipt'),
	path('sales-report/', sales_report, name='sales_report'),
 
]