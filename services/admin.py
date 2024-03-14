from django.contrib import admin
from .models import *

admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceBooking)
admin.site.register(InstallerAssignment)


class AssignedServiceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'service', 
        'installer',
        'status',
        'date_assigned',
    )
    list_filter = (
        'service',
        'installer',
        'status',
    )
    
admin.site.register(AssignedServiceBooking, AssignedServiceBookingAdmin)
