from django.urls import path
from .views import email_login_view, otp_verify_view,logout_view

urlpatterns = [
    path('', email_login_view, name='email_login'),
    path('verify-otp/', otp_verify_view, name='otp_verify'),
     path('logout/', logout_view, name='logout'),
]
