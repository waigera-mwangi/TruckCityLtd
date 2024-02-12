from django import forms
from .models import OrderPayment
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
    class Meta:
        model = OrderPayment
        fields = ['county','town','phone_number']
        widgets = {
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'town': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            
        }