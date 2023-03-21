from django import forms
from .models import Host, EndUser, Vehicle, Rents, Travelogue, ReportUser, report_status
from django.forms import DateTimeInput
from django.db.models import Q


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
        exclude = ['by', 'to', 'status']


class ReportFilterForm(forms.Form):
    status = forms.ChoiceField(choices=report_status)
    # def init(self, *args, **kwargs):
    #     super().init(*args, **kwargs)
    #     self.fields['name'].widget.attrs.update({'class': 'first_name'})

    def filter_report(self, queryset):
        status = self.cleaned_data['status']
        if status:
            queryset = queryset.filter(
                status=status
            )
        return queryset


class UserFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Enter name'}))

    def filter_users(self, queryset):
        name = self.cleaned_data['name']
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            )
        return queryset

class UserFilterStatusForm(forms.Form):
    status = forms.ChoiceField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')])

    def filter_users(self, queryset):
        status = self.cleaned_data['status']
        if status:
            print(status)
            print(queryset)
            queryset = queryset.filter(
                is_approved=status
            )
            print(queryset)
        return queryset