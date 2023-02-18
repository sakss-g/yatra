from django import forms
from .models import Host, EndUser, Vehicle

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

class VehicleUpdateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['is_approved', 'host']
        # fields = ['first_name', 'last_name', 'address', 'phone_number', 'pic']