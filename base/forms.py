from django import forms
from .models import Host, EndUser

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