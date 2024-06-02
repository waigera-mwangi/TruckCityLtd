# supply/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SupplyTender
from finance.models import TenderPayment


@receiver(post_save, sender=SupplyTender)
def create_tender_payment(sender, instance, created, **kwargs):
    # Check if the status is "Paid" and if the payment hasn't already been created
    if instance.tender_status == 'Paid' and not hasattr(instance, 'payment'):
        TenderPayment.objects.create(
            supply_tender=instance,
            paid_to=instance.user
        )