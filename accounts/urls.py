from django.urls import path, reverse_lazy
from accounts import views
from accounts.views import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from accounts.decorators import required_access
from store.views import *

app_name = "accounts"

urlpatterns = [
    path('register/', UserCreateView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    
    path('', views.loginView, name='login'),
    path('customer/', views.customer, name='customer'),
    path('driver/', views.driver, name='driver'),
    path('inventory_manager/', views.inventory_manager, name='inventory_manager'),
    path('service_provider/', views.service_provider, name='service_provider'),
    path('installer/', views.installer, name='installer'),
    path('supplier/', views.supplier, name='supplier'),
    path('finance-manager/', views.finance_manager, name='finance_manager'),
    
]
