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
    list_display = ('id', 'order', 'delivery_date', 'status', 'driver',)
    list_filter = ('delivery_date', )
    search_fields = ('name', 'order')
    readonly_fields = ('delivery_date',)
admin.site.register(Shipping, ShippingAdmin)
