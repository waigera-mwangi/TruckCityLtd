from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from .models import Shipping




# class LocationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at', 'updated_at',)
#     list_filter = ('created_at', 'updated_at',)
#     search_fields = ('name',)
#     readonly_fields = ('created_at', 'updated_at',)


# class PickUpStationAdmin(admin.ModelAdmin):
#     list_display = ( 'location', 'created_at', 'updated_at',)
#     list_filter = ('created_at', 'updated_at',)
#     search_fields = ()
#     readonly_fields = ('created_at', 'updated_at',)


# class UserPickUpStationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'station', 'location', 'created_at', 'updated_at',)
#     list_filter = ('created_at', 'updated_at')
#     search_fields = ('user')
#     readonly_fields = ('created_at', 'updated_at',)

#     def location(self, obj):
#         return obj.station.location.name


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_user', 'delivery_date', 'status', 'driver')
    list_filter = ('delivery_date', )
    search_fields = ('order__user__username', 'order__id')
    readonly_fields = ('delivery_date',)

    # Custom method to get the username of the order user
    def order_user(self, obj):
        return obj.order.user.username

    # Custom method to get the order ID
    def order_id(self, obj):
        return obj.order.id

    # Add column names for admin display
    order_user.short_description = 'Customer'
    order_id.short_description = 'Order ID'

admin.site.register(Shipping, ShippingAdmin)
