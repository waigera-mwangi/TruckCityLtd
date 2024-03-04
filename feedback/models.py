from django.db import models
from accounts.models import User,CustomPhoneNumberField,TimeStamp
from django.utils.translation import gettext_lazy as _

# faq's
class FAQ(TimeStamp):
    class QustionType(models.TextChoices):
        DRIVER = 'DR', _('Driver')
        FINANCE_MANAGER = 'FM', _('Finance Manager')
        INVENTORY_MANAGER = 'IM', _('Inventory Manager')
        SUPPLIER = 'SR', _('Supplier')
        CUSTOMER = 'CM', _('Customer')
        INSTALLER = 'IS', _('Installer')
        SERVICE_PROVIDER = 'SP', _('Service Provider')
        
    question_types = models.CharField(
        _('question Type'),
        max_length=3,
        choices=QustionType.choices,
        default=QustionType.CUSTOMER
    )
    subject = models.CharField( max_length=250)
    content = models.TextField()

# feedback
      
class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_feedbacks')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedbacks')
    message = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.sender.get_full_name()} to {self.receiver.get_full_name()}"
    
    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        
    
