from django import forms
from .models import ACRequest, WaterPurifierRequest, ChimneyHobRequest,Customer,RequestForm

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = RequestForm
        fields = [
            'status',
            'start_date',
            'third_party_worker_name',
            'payment_method',
        ]

        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'third_party_worker_name': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        
class SelectExistingCustomerForm(forms.Form):
    existing_customer = forms.ModelChoiceField(
        queryset=Customer.objects.none(),
        required=False,
        label='Select Existing Customer',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['existing_customer'].queryset = Customer.objects.filter(created_by=user)


class CustomerDetailsForm(forms.Form):
    customer_name = forms.CharField(
        label='Full Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'})
    )
    customer_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    customer_phone = forms.CharField(
        label='Phone Number',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
    )
    customer_address = forms.CharField(
        label='Address',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address', 'rows': 3})
    )

class acRequestForm(forms.ModelForm):
    class Meta:
        model = ACRequest
        fields = ['comprensive', 'ac_type', 'product_brand', 'amc_years']
        widgets = {
            'comprensive': forms.Select(attrs={'class': 'form-select'}),
            'ac_type': forms.Select(attrs={'class': 'form-select'}),
            'product_brand': forms.Select(attrs={'class': 'form-select'}),  # fixed here
            'amc_years': forms.Select(attrs={'class': 'form-select'}),
        }

class WaterPurifierRequestForm(forms.ModelForm):
    class Meta:
        model = WaterPurifierRequest
        fields = ['comprensive', 'purifier_type', 'product_brand', 'amc_years']
        widgets = {
            'comprensive': forms.Select(attrs={'class': 'form-select'}),
            'purifier_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RO, UV'}),
            'product_brand': forms.Select(attrs={'class': 'form-select'}),  # fixed here
            'amc_years': forms.Select(attrs={'class': 'form-select'}),
        }

class ChimneyHobRequestForm(forms.ModelForm):
    class Meta:
        model = ChimneyHobRequest
        fields = ['comprensive', 'device_type', 'product_brand', 'amc_years']
        widgets = {
            'comprensive': forms.Select(attrs={'class': 'form-select'}),
            'device_type': forms.Select(attrs={'class': 'form-select'}),
            'product_brand': forms.Select(attrs={'class': 'form-select'}),  # fixed here
            'amc_years': forms.Select(attrs={'class': 'form-select'}),
        }

