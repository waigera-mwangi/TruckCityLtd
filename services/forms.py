from django import forms
from django.forms.widgets import DateInput
from .models import *
import re
from django import forms
from django import forms
from django.core.exceptions import ValidationError
from datetime import date

class BookingServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['booking_date']
        labels = {
            'booking_date': 'Booking Date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['booking_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date < date.today():
            raise ValidationError("Booking date must be a present or future date.")
        return booking_date
