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
    tools_required = models.TextField(null=True, blank=True) 
   
    class Meta:
        managed = True
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
           
    
    def __str__(self):
        return self.name.name

# services bookedclass ServiceBooking(models.Model):
class ServiceBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    LOCATION_CHOICES = [
        ('kitale', 'Kitale'),
        ('eldoret', 'Eldoret'),
        ('iten', 'Iten'),
        ('marigat', 'Marigat'),
        ('kericho', 'Kericho'),
        # Add more towns as needed
    ]
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    booking_date = models.DateField()
    tools_required = models.TextField(null=True, blank=True)
    service_delivered = models.BooleanField(default=False)
    customer_feedback = models.TextField(null=True, blank=True)
    customer_approval = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'Service Booking'
        verbose_name_plural = 'Service Bookings'

    def __str__(self):
        return f"Booking #{self.pk} - {self.service}"

# assigned bookings

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
    tools_requested = models.BooleanField(default=False)
    tools_provided = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Assigned Service Booking'
        verbose_name_plural = 'Assigned Service Bookings'

    def __str__(self):
        return f"{self.booking} - Assigned to: {self.installer}"
