from django import forms
from .models import ServiceBooking

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the form fields if needed
        # For example, add a date field for booking_date
