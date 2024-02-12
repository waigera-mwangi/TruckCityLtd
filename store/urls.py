from store import views

from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    # customer
    path('view-products/',ProductView.as_view(), name='view-products'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('customer-order-list/', customer_order_list, name='customer-order-list'),
    path('customer-order-details/<int:order_id>/', customer_order_detail, name='customer-order-details'),
    path('customer-invoice/', customer_order_invoice, name='customer-invoice'),
    path('order/<int:order_id>/pdf/', views.customer_order_pdf, name='customer-order-pdf'),
    
    # finance manager
    path('approve-payment/<str:transaction_id>/', approve_payment, name='approve_payment'),
    path('pending-orders/', pending_orders, name='pending_orders'),
    path('approved-orders/', approved_orders, name='approved_orders'),
    path('rejected-orders/', order_rejected_payment, name='rejected_orders'),
    
    # service provider
    path('assign-order-list/', assign_driver_order_list, name='assign-order-list'),
    path('assigned-order-list/', assigned_order_list, name='assigned-order-list'),


#   inventory
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-detail/<int:pk>/', ProductDetailViewCustomer.as_view(), name='product-detail-customer'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('create_category/', views.create_category, name='create_category'),
    path('inventory_category_list/', views.inventory_category_list, name='inventory_category_list'),
    path('update_category/<str:pk>/', views.update_category, name='update_category'),
    
]
 