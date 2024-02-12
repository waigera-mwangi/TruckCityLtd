from django.contrib import admin

from .models import *


class SupplyTenderAdmin(admin.ModelAdmin):
    list_display =('product','quantity','date','tender_status','user')


admin.site.register(SupplyTender, SupplyTenderAdmin)