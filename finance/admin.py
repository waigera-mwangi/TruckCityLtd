from django.contrib import admin
from .models import *


class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 
                    'get_user', 
                    'payment_status',
                    'county', 
                    'town',
                    'phone_number',
                    'payment_date')

    
    def get_user(self, obj):
        return obj.order.user

    get_user.short_description = 'User'


admin.site.register(OrderPayment, OrderPaymentAdmin)

class BooKingPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id',
                    'location',
                    'address',
                    'payment_status',
                    'payment_date',
                    )
    list_filter = (
        'payment_date', 
        'payment_status',
    )
admin.site.register(BooKingPayment, BooKingPaymentAdmin)