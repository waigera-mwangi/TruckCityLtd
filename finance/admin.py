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
                    'user',
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


class TenderPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'supply_tender', 'payment_date', 'paid_to', 'display_amount')
    list_filter = ('payment_date',)
    search_fields = ('supply_tender__product__name', 'paid_by__username')

    def display_amount(self, obj):
        return obj.amount
    display_amount.short_description = 'Amount'

admin.site.register(TenderPayment, TenderPaymentAdmin)