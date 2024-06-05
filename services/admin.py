from django.contrib import admin
from .models import *

admin.site.register(ServiceCategory)
admin.site.register(Service)



class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'service',
        'location',
        'booking_date',
        'tools_required'
    )
    
    list_filter = (
        'service',
        'user',
        'location'
    )
    
admin.site.register(ServiceBooking, ServiceBookingAdmin)

class InstallerAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'booking',
        'installer',
        'date', 
        'status', 
        'tools_requested',
        'tools_provided'
    )
    
    list_filter = (
        'booking',
        'installer',
        'status'
    )
    
    
admin.site.register(InstallerAssignment)