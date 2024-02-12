from django import forms
# from .models import Location, PickUpStation, UserPickUpStation, Shipping
from .models import  Shipping


# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = ['name']


# class PickUpStationForm(forms.ModelForm):
#     class Meta:
#         model = PickUpStation
#         fields = ['name', 'location']


# class UserPickUpStationForm(forms.ModelForm):
#     station = forms.ModelChoiceField(
#         queryset=PickUpStation.objects.all(),
#         label='Pickup Station',
#         widget=forms.Select(attrs={'class': 'form-select'}),
#         to_field_name='id',
#         empty_label=None,
#     )

#     class Meta:
#         model = UserPickUpStation
#         fields = ['station']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['station'].label_from_instance = lambda obj: f"{obj.name} ({obj.location.name})"


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['order', 'status', 'driver']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['station'].label_from_instance = lambda obj: f"{obj.station.name} ({obj.station.location.name})"

