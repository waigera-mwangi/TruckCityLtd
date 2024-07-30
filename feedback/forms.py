from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, logout
from django.forms import forms, ModelForm
from django import forms
from accounts.models import *
from .models import *
User = get_user_model()

# customer feedback form
class CustomerFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.DRIVER, 
                                                                                  User.UserTypes.SERVICE_PROVIDER, 
                                                                                  User.UserTypes.INSTALLER]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.DRIVER, 
                                                                                  User.UserTypes.SERVICE_PROVIDER, 
                                                                                  User.UserTypes.INSTALLER])

# finance feedback form
class FinanceFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.CUSTOMER, 
                                                                                  User.UserTypes.INVENTORY_MANAGER,
                                                                                  User.UserTypes.INSTALLER,
                                                                                  User.UserTypes.SUPPLIER,
                                                                                  ]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.CUSTOMER, 
                                                                                  User.UserTypes.INVENTORY_MANAGER,
                                                                                  User.UserTypes.INSTALLER,
                                                                                  User.UserTypes.SUPPLIER,
                                                                                  ])

# inventory feedback form
class InventoryFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.SERVICE_PROVIDER, 
                                                                                  User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.INSTALLER,
                                                                                  User.UserTypes.SUPPLIER,
                                                                                  ]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.SERVICE_PROVIDER, 
                                                                                  User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.INSTALLER,
                                                                                  User.UserTypes.SUPPLIER,
                                                                                  ])


# installer feedback form
class InstallerFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.SERVICE_PROVIDER, 
                                                                                  User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.CUSTOMER,
                                                                                  User.UserTypes.INVENTORY_MANAGER,
                                                                                  ]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.SERVICE_PROVIDER, 
                                                                                  User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.CUSTOMER,
                                                                                  User.UserTypes.INVENTORY_MANAGER,
                                                                                  ])

# supplier feedback form
class SupplierFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.INVENTORY_MANAGER]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.FINANCE_MANAGER,
                                                                                  User.UserTypes.INVENTORY_MANAGER])


# dispatch feedback form
class ServiceFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.CUSTOMER,
                                                                                  User.UserTypes.FINANCE_MANAGER, 
                                                                                  User.UserTypes.INSTALLER, 
                                                                                  User.UserTypes.DRIVER]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.CUSTOMER,
                                                                                  User.UserTypes.FINANCE_MANAGER, 
                                                                                  User.UserTypes.INSTALLER, 
                                                                                  User.UserTypes.DRIVER])

# driver feedback form
class DriverFeedbackForm(forms.Form):
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[User.UserTypes.CUSTOMER,
                                                                                  User.UserTypes.SERVICE_PROVIDER]))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(user_type__in=[User.UserTypes.CUSTOMER,
                                                                                  User.UserTypes.SERVICE_PROVIDER])


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'phone_number', 'message']