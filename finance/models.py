from django.db import models
from accounts.models import User
from store.models import Order
from phonenumber_field.modelfields import PhoneNumberField
from supply.models import SupplyTender
from services.models import * 
class CustomPhoneNumberField(PhoneNumberField):
    default_error_messages = {
        'invalid': 'Please enter a valid phone number in the format +254723000000.',
    }

# Create your models here.
class OrderPayment(models.Model):
    class Meta:
        verbose_name = 'Order Payment'
        verbose_name_plural = 'Order Payments'

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    phone_number = CustomPhoneNumberField(null=True)

class BooKingPayment(models.Model):
    class Meta:
        verbose_name = 'Booking Payment'
        verbose_name_plural = 'Booking Payments'
        
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]
    booking = models.OneToOneField(ServiceBooking, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    location = models.CharField(max_length=50)
    address = models.IntegerField(null=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateField(auto_now_add=True)
    

# finance model to view paid tenders
class TenderPayment(models.Model):
    supply_tender = models.OneToOneField(SupplyTender, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateField(auto_now_add=True)
    paid_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    @property
    def amount(self):
        return self.supply_tender.price * self.supply_tender.quantity

    def __str__(self):
        return f"Payment for {self.supply_tender}"