from django.contrib import admin
from .models import Product, Order, OrderItem, Category
from finance.models import OrderPayment
from django.apps import apps
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'price', 'quantity', 'created_date', 'description')
 
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_transaction_id','is_completed', 'order_date',)
    list_filter = ('order_date', 'is_completed')
    search_fields = ('id', 'user__username')
    readonly_fields = ('order_date',)
    inlines = [OrderItemInline]
    raw_id_fields = ('user', 'pole')
    

    def get_transaction_id(self, obj):
        OrderPayment = apps.get_model('finance', 'OrderPayment')
        try:
            payment = OrderPayment.objects.get(order=obj)
            return payment.transaction_id
        except OrderPayment.DoesNotExist:
            return 'N/A'

    get_transaction_id.short_description = 'Transaction ID'
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
# admin.site.register(OrderItem)