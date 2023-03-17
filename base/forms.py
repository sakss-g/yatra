from django import forms
from .models import Host, EndUser, Vehicle, Rents, Travelogue, ReportUser
from django.forms import DateTimeInput
class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['first_name', 'last_name', 'email']


class EndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ['first_name', 'last_name', 'email']


class EndUserUpdateForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ['first_name', 'last_name', 'phone_number', 'pic']


class HostUpdateForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'pic']


class EndUserDocumentsForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ['citizenship_id', 'citizenship', 'license_no', 'license' ]


class HostDocumentsForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['citizenship_id', 'citizenship' ]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['host', "is_approved"]


class RentVehicle(forms.ModelForm):
    class Meta:
        model = Rents
        exclude = ['vehicle', 'renter']
        widgets = {
            'date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SubmitTravelogueForm(forms.ModelForm):
    class Meta:
        model = Travelogue 
        exclude = ['enduser', 'is_approved']


class ReportUserForm(forms.ModelForm):
    class Meta:
        model = ReportUser
        exclude = ['by', 'to']