from django import forms
from .models import Host, EndUser, Vehicle, Rents, Travelogue, ReportUser,RateRent, report_status, status, FAQs, TermsAndConditions,PrivacyPolicy
from django.forms import DateTimeInput
from django.db.models import Q


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class EndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']


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

class FAQsForm(forms.ModelForm):
    class Meta:
        model = FAQs 
        fields = ['question', 'answer']

class TermsAndConditionsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions 
        fields = ['term', 'explanation']

class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy 
        fields = ['policy', 'explanation']    

class ReportUserForm(forms.ModelForm):
    class Meta:
        model = ReportUser
        exclude = ['by', 'to', 'status']


class RateRentForm(forms.ModelForm):
    class Meta:
        model = RateRent
        exclude = ['rent']


class ReportFilterForm(forms.Form):
    status = forms.ChoiceField(choices=report_status)

    def filter_report(self, queryset):
        status = self.cleaned_data['status']
        if status:
            queryset = queryset.filter(
                status=status
            )
        return queryset


class UserFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Enter first or last name'}))

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
    
class StatusFilterForm(forms.Form):
    is_approved = forms.ChoiceField(choices=status)

    def filter_report(self, queryset):
        is_approved = self.cleaned_data['is_approved']
        if is_approved:
            queryset = queryset.filter(
                is_approved=is_approved
            )
        return queryset