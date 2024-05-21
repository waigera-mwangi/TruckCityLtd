from django import forms
from django.forms.widgets import DateInput
from .models import *
import re
from django.core.exceptions import ValidationError
from datetime import date
from django import forms
class BookingServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['booking_date', 'location']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date < date.today():
            raise forms.ValidationError("Booking date must be a present or future date.")
        return booking_date
    
class ToolRequestForm(forms.Form):
    # This form can be extended if you need more fields
    confirm_request = forms.BooleanField(required=True, label="Confirm tool request")


class ToolAssignmentForm(forms.Form):
    confirm_provide_tools = forms.BooleanField(required=True, label="Confirm tool provision")