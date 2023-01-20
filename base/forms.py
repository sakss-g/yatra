from django import forms
from .models import Host

class Form(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['first_name', 'last_name', 'email']
