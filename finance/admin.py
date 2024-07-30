from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import OrderPayment, BooKingPayment, TenderPayment

def export_to_pdf_order_payments(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=order_payments.pdf'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 40, "Truck City Limited")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 60, "Order Payments Report")
    p.setFont("Helvetica-Bold", 12)
    y = height - 80
    headers = ['Transaction ID', 'Payment Status', 'County', 'Town', 'Phone Number', 'Payment Date']
    for i, header in enumerate(headers):
        p.drawString(50 + i * 100, y, header)
    p.setFont("Helvetica", 10)
    for obj in queryset:
        y -= 20
        row = [obj.transaction_id, obj.payment_status, obj.county, obj.town, str(obj.phone_number), str(obj.payment_date)]
        for i, value in enumerate(row):
            p.drawString(50 + i * 100, y, value)
    p.showPage()
    p.save()
    return response

def export_to_pdf_booking_payments(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=booking_payments.pdf'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 40, "Truck City Limited")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 60, "Booking Payments Report")
    p.setFont("Helvetica-Bold", 12)
    y = height - 80
    headers = ['Transaction ID', 'User', 'Location', 'Address', 'Payment Status', 'Payment Date']
    for i, header in enumerate(headers):
        p.drawString(50 + i * 100, y, header)
    p.setFont("Helvetica", 10)
    for obj in queryset:
        y -= 20
        row = [obj.transaction_id, obj.user.username, obj.location, str(obj.address), obj.payment_status, str(obj.payment_date)]
        for i, value in enumerate(row):
            p.drawString(50 + i * 100, y, value)
    p.showPage()
    p.save()
    return response

def export_to_pdf_tender_payments(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=tender_payments.pdf'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 40, "Truck City Limited")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 60, "Tender Payments Report")
    p.setFont("Helvetica-Bold", 12)
    y = height - 80
    headers = ['ID', 'Supply Tender', 'Payment Date', 'Paid To', 'Amount']
    for i, header in enumerate(headers):
        p.drawString(50 + i * 100, y, header)
    p.setFont("Helvetica", 10)
    for obj in queryset:
        y -= 20
        row = [str(obj.id), str(obj.supply_tender), str(obj.payment_date), obj.paid_to.username, str(obj.amount)]
        for i, value in enumerate(row):
            p.drawString(50 + i * 100, y, value)
    p.showPage()
    p.save()
    return response

class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'payment_status', 'county', 'town', 'phone_number', 'payment_date')
    actions = [export_to_pdf_order_payments]

admin.site.register(OrderPayment, OrderPaymentAdmin)

class BooKingPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'location', 'address', 'payment_status', 'payment_date')
    list_filter = ('payment_date', 'payment_status')
    actions = [export_to_pdf_booking_payments]

admin.site.register(BooKingPayment, BooKingPaymentAdmin)

class TenderPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'supply_tender', 'payment_date', 'paid_to', 'display_amount')
    list_filter = ('payment_date',)
    search_fields = ('supply_tender__product__name', 'paid_to__username')
    actions = [export_to_pdf_tender_payments]

    def display_amount(self, obj):
        return obj.amount
    display_amount.short_description = 'Amount'

admin.site.register(TenderPayment, TenderPaymentAdmin)
