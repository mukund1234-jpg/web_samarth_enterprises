from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from .models import CustomUser, OTP
from .forms import EmailForm, OTPForm
from django.conf import settings
from django.contrib.auth.decorators import login_required


def send_otp_email(email, code):
    send_mail(
        'Your Login OTP',
        f'Your OTP is: {code}',
        settings.DEFAULT_FROM_EMAIL,  # Sends from your app's Gmail
        [email],                      # Sends to user-entered email
        fail_silently=False,
    )


def email_login_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'User not found.'})
            otp, created = OTP.objects.get_or_create(user=user)
            otp.generate_otp()
            send_otp_email(email, otp.code)
            request.session['email'] = email
            return redirect('otp_verify')
    else:
        form = EmailForm()
    return render(request, 'accounts/login.html', {'form': form})

def otp_verify_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('email_login')

    user = CustomUser.objects.get(email=email)
    otp_obj = OTP.objects.get(user=user)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == otp_obj.code:
                login(request, user)
                if user.role == 'admin':
                    return redirect('dashboard')
                elif user.role == 'office_worker':
                    return redirect('dashboard')
                elif user.role == 'customer':
                    return redirect('dashboard')
            else:
                return render(request, 'accounts/otp_verify.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        form = OTPForm()
    return render(request, 'accounts/otp_verify.html', {'form': form})


def logout_view(request):
    logout(request)  # Clears session and logs out the user
    return redirect('email_login')#t to your email login page
