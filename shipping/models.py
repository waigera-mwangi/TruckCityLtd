from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from store.models import Order
from django.contrib.auth import get_user_model
class Shipping(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PD', _('Pending')
        OUT_FOR_DELIVERY = 'OFD', _('Out For Delivery')
        DELIVERED = 'DL', _('Delivered')
        COMPLETE = 'CL', _('Complete')

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_date = models.DateField(auto_now_add=True, verbose_name='shipped_date')
    status = models.CharField(_('status'), max_length=3, choices=Status.choices, default=Status.PENDING)
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='shipments_as_driver')

    def __str__(self):
        return f'Shipping #{self.id}'

    def get_status_display(self):
        return dict(Shipping.Status.choices)[self.status]
    
    class Meta:
        verbose_name_plural = 'Ordered Pole Shipment'
    