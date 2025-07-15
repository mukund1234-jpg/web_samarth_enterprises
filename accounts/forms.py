from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control glass-input',
            'placeholder': 'Enter your email',
            'autocomplete': 'email',
        }),
        help_text="We'll send a one-time password (OTP) to this email."
    )

class OTPForm(forms.Form):
    otp = forms.CharField(
        label="One-Time Password (OTP)",
        max_length=6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control glass-input',
            'placeholder': 'Enter OTP',
            'inputmode': 'numeric',
            'autocomplete': 'one-time-code',
        }),
        help_text="Enter the 6-digit OTP sent to your email."
    )