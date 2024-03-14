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
    name = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null = True)
    image = models.ImageField(null=False)
    description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')
    
    class Meta:
        managed = True
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
           
    
    def __str__(self):
        return self.name.name

# services booked
class ServiceBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Booking'
        verbose_name_plural = 'Service Bookings'

    def __str__(self):
        return f"Booking #{self.pk} - {self.service}"
    
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
    
class InstallerAssignment(models.Model):
    class AssignmentStatus(models.TextChoices):
        ASSIGNED = 'assigned', 'Assigned'
        COMPLETED = 'completed', 'Completed'

    booking = models.OneToOneField(ServiceBooking, on_delete=models.CASCADE, related_name='installer_assignment')
    installer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ASSIGNED
    )

    class Meta:
        verbose_name = 'Assigned Service Booking'
        verbose_name_plural = 'Assigned Service Bookings'

    def __str__(self):
        return f"{self.booking} - Assigned to: {self.installer}"
