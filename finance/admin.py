from django.contrib import admin
from .models import *


class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 
                    'user', 'payment_status', 'county', 'town',
                    'phone_number','payment_date')


    def user(self, obj):
    	return obj.order.user


admin.site.register(OrderPayment, OrderPaymentAdmin)

class BooKingPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id',
                    'user',
                    'location',
                    'payment_status',
                    'payment_date',
                    )
    list_filter = (
        'user',
        'payment_date', 
        'payment_status',
    )
admin.site.register(BooKingPayment, BooKingPaymentAdmin)