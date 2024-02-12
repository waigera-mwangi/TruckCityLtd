from django.db import models
from djmoney.models.fields import MoneyField
from accounts.models import User
from django.utils.translation import gettext_lazy as _

# categories for services
class ServiceCategory(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        
    name = models.CharField(max_length=50, default='Pole installation')
    price = MoneyField(max_digits=10,decimal_places=2, default_currency='KES', verbose_name='Cost per day')
    
    
    def __str__(self):
        return self.name
    
# services from categories
class Service(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        
    name = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null = True)
    image = models.ImageField(null=False)
    description = models.TextField()
    price = MoneyField(max_digits=10,decimal_places=2, default_currency='KES', verbose_name='Cost per day', null = True)
    
    def __str__(self):
        return self.name

# services booked
class ServiceBooking(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Services Booking'
        verbose_name_plural = 'Services Bookings'
        
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now=True)
    
# assigned bookings
class AssignedServiceBooking(models.Model):
    class  Meta:
        db_table = ''
        managed = True
        verbose_name = 'Assigned service'
        verbose_name_plural = 'Assigned services'
        
    class assign_status(models.TextChoices):
        Assigned = 'AS', _('Assigned')
        Completed = 'CP', _('Completed')
        
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=False)
    date_assigned = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=5,choices=assign_status.choices, default=assign_status.Assigned)
    installer =  models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    