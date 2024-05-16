from django import forms
from .models import *
import re
from django.core.validators import RegexValidator

def alphanumeric_mixed_validator(value):
    if not value.isalnum() or not any(char.isdigit() for char in value) or not any(char.isalpha() for char in value):
        raise forms.ValidationError('The transaction ID must be a minimum of 8 characters and contain a mixture of letters and numbers.')

class PaymentForm(forms.Form):
    transaction_id = forms.CharField(
        min_length=8,
        validators=[alphanumeric_mixed_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class AddressForm(forms.ModelForm):
    alphanumeric_validator = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters are allowed.')
    
    COUNTY_CHOICES = [
        ('transnzoia', 'Trans-Nzoia'),
        ('uasingishu', 'Uasin Gishu'),
        ('elgeyomarakwet', 'Elgeyo-Marakwet'),
        ('baringo', 'Baringo'),
        ('kericho', 'Kericho'),
        # Add more towns as needed
    ]

    # Define the town field as a ChoiceField with Select widget
    county = forms.ChoiceField(choices=COUNTY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    TOWN_CHOICES = [
        ('kitale', 'Kitale'),
        ('eldoret', 'Eldoret'),
        ('iten', 'Iten'),
        ('marigat', 'Marigat'),
        ('kericho', 'kericho'),
        # Add more towns as needed
    ]

    # Define the town field as a ChoiceField with Select widget
    town = forms.ChoiceField(choices=TOWN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = OrderPayment
        fields = ['county','town','phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        

class BookingPaymentForm(forms.ModelForm):
    class Meta:
        model = BooKingPayment
        fields = ['location', 'address', 'transaction_id']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['transaction_id'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter A Valid Mpesa Code',
            'pattern': '^[A-Z\d]{8}$',
            'title': 'The Mpesa Code should be 8 characters long and in all caps'
        })
