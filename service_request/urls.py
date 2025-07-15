from django.urls import path
from .views import *

urlpatterns = [
       path('dashboard/', dashboard, name='dashboard'),
       path('service/', service, name='service'),
       path('about-us/',aboutus, name='about'),
       path('service-request/<slug:category_slug>/', request_form_view, name='request_form'),
       path('services/<str:category>/<uuid:uuid>/', service_details, name='service_details'),
       path('update-status/<uuid:uuid>/', update_status_view, name='update_status'),
       path('service-search/', service_search_results, name='service_search_results'),
       path('profile/',profile_view, name='profile'),


]
