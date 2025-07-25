from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerDetailsForm, acRequestForm, WaterPurifierRequestForm, ChimneyHobRequestForm, SelectExistingCustomerForm,RequestForm
from .models import User, Customer, ProductCategory
from django.contrib.auth import get_user_model
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from .forms import StatusUpdateForm
from .utils import generate_pdf_receipt
from .models import ACRequest, WaterPurifierRequest, ChimneyHobRequest
from django.utils.timezone import localtime, now
from datetime import timedelta
from django.core.files.base import ContentFile



User = get_user_model()



from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    user = request.user
    tab = request.GET.get('tab', 'pending')  # 'pending' or 'complete'

    # Filter by user role
    if user.role == 'office_worker':
        ac_requests = list(ACRequest.objects.filter(customer__created_by=user))
        wp_requests = list(WaterPurifierRequest.objects.filter(customer__created_by=user))
        ch_requests = list(ChimneyHobRequest.objects.filter(customer__created_by=user))
    elif user.role == 'customer':
        ac_requests = list(ACRequest.objects.filter(customer__user=user))
        wp_requests = list(WaterPurifierRequest.objects.filter(customer__user=user))
        ch_requests = list(ChimneyHobRequest.objects.filter(customer__user=user))
    else:
        ac_requests = list(ACRequest.objects.all())
        wp_requests = list(WaterPurifierRequest.objects.all())
        ch_requests = list(ChimneyHobRequest.objects.all())

    # Combine and label
    all_requests = ac_requests + wp_requests + ch_requests

    for req in all_requests:
        if isinstance(req, ACRequest):
            req.category_slug = 'air-conditioner'
        elif isinstance(req, WaterPurifierRequest):
            req.category_slug = 'water-filter'
        elif isinstance(req, ChimneyHobRequest):
            req.category_slug = 'chimaney-hub'

        today = localtime(now()).date()
        created_date = localtime(req.created_at).date()
        if created_date == today:
            req.display_date = "Today"
        elif created_date == today - timedelta(days=1):
            req.display_date = "Yesterday"
        else:
            req.display_date = created_date.strftime("%d %b %Y")

    # Filter by tab (status)
    if tab == 'complete':
        filtered_requests = [r for r in all_requests if r.status == 'Completed']
    else:
        filtered_requests = [r for r in all_requests if r.status == 'Pending']

    return render(request, 'amc/homePage.html', {
        'requests': filtered_requests,
        'tab': tab
    })


@login_required
def service_details(request, category, uuid):
    if category == 'air-conditioner':
        service = get_object_or_404(ACRequest, uuid=uuid)
    elif category == 'water-filter':
        service = get_object_or_404(WaterPurifierRequest, uuid=uuid)
    elif category == 'chimaney-hub':
        service = get_object_or_404(ChimneyHobRequest, uuid=uuid)
    else:
        return redirect('dashboard')

    # Directly use the URL string stored in service.bill
    bill_url = service.bill_url if service.bill_url else ''

    return render(request, 'amc/service_detailsPage.html', {
        'service': service,
        'category': category,
        'bill_url': bill_url
    })

@login_required
def service(request):
    service= ProductCategory.objects.all()
    return render(request,'amc/servicePage.html',{'service':service})


def aboutus(request):
    return render(request,'amc/aboutusPage.html')

@login_required
def request_form_view(request, category_slug):
    CATEGORY_FORM_MAP = {
        'air-conditioner': acRequestForm,
        'water-filter': WaterPurifierRequestForm,
        'chimaney-hub': ChimneyHobRequestForm,
    }

    service_form_class = CATEGORY_FORM_MAP.get(category_slug.lower())
    if not service_form_class:
        return redirect('dashboard')

    try:
        category_obj = ProductCategory.objects.get(slug=category_slug)
    except ProductCategory.DoesNotExist:
        return redirect('dashboard')

    pricing_rules = {
        "1": {"price": 1000, "visits": 3},
        "3": {"price": 3000, "visits": 9},
        "comprensive_addon": 300
    }

    if request.method == 'POST':
        select_customer_form = SelectExistingCustomerForm(request.POST, user=request.user)
        customer_form = CustomerDetailsForm(request.POST)
        service_form = service_form_class(request.POST)

        customer = None

        if select_customer_form.is_valid():
            selected_customer = select_customer_form.cleaned_data.get('existing_customer')
            if selected_customer:
                customer = selected_customer

        if not customer and customer_form.is_valid():
            email = customer_form.cleaned_data['customer_email']
            phone = customer_form.cleaned_data['customer_phone']
            address = customer_form.cleaned_data['customer_address']
            name = customer_form.cleaned_data['customer_name']

            user, created = User.objects.get_or_create(
                email=email,
                defaults={'role': 'customer', 'name': name}
            )
            if created:
                user.set_unusable_password()
                user.save()

            customer, _ = Customer.objects.get_or_create(user=user, defaults={
                'phone': phone,
                'address': address,
                'created_by': request.user,
            })

        if not customer or not service_form.is_valid():
            customers = Customer.objects.filter(created_by=request.user).select_related('user')
            customer_data = {
                str(c.id): {
                    'name': c.user.name,
                    'email': c.user.email,
                    'phone': c.phone,
                    'address': c.address,
                } for c in customers
            }

            return render(request, 'amc/service_formPage.html', {
                'select_customer_form': select_customer_form,
                'customer_form': customer_form,
                'service_form': service_form,
                'category': category_slug,
                'customer_data_json': json.dumps(customer_data, cls=DjangoJSONEncoder),
                'pricing_rules': json.dumps(pricing_rules),
                'error': "Please fix the errors in the form."
            })

        request_obj = service_form.save(commit=False)
        request_obj.customer = customer
        request_obj.created_by = request.user
        request_obj.category = category_obj
        request_obj.save()

        return redirect('dashboard')

    else:
        select_customer_form = SelectExistingCustomerForm(user=request.user)
        customer_form = CustomerDetailsForm()
        service_form = service_form_class()

        customers = Customer.objects.filter(created_by=request.user).select_related('user')
        customer_data = {
            str(c.id): {
                'name': c.user.name,
                'email': c.user.email,
                'phone': c.phone,
                'address': c.address,
            } for c in customers
        }

        return render(request, 'amc/service_formPage.html', {
            'select_customer_form': select_customer_form,
            'customer_form': customer_form,
            'service_form': service_form,
            'category': category_slug,
            'customer_data_json': json.dumps(customer_data, cls=DjangoJSONEncoder),
            'pricing_rules': json.dumps(pricing_rules),
        })

@login_required
def update_status_view(request, uuid):
    base_service = get_object_or_404(RequestForm, uuid=uuid)

    # 🔁 Get child instance (ACRequest, WaterPurifierRequest, etc.)
    if hasattr(base_service, 'acrequest'):
        service = base_service.acrequest
    elif hasattr(base_service, 'waterpurifierrequest'):
        service = base_service.waterpurifierrequest
    elif hasattr(base_service, 'chimneyhobrequest'):
        service = base_service.chimneyhobrequest
    else:
        service = base_service  # fallback (very rare)

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            updated_service = form.save(commit=False)

            if updated_service.status == "Completed":
                # ✅ Now amc_years will be accessible
                if updated_service.start_date and hasattr(updated_service, 'amc_years'):
                    updated_service.end_date = updated_service.start_date + timedelta(days=365 * updated_service.amc_years)

            updated_service.save()  # ✅ Will call subclass save() and calculate price, visits

            if updated_service.status == "Completed":
                pdf_file = generate_pdf_receipt(updated_service)
                filename = f"receipt_{updated_service.id}.pdf"
                updated_service.bill_url.save(filename, ContentFile(pdf_file.getvalue()))
                updated_service.save()

            return redirect('service_details', category=updated_service.category.slug.lower(), uuid=updated_service.uuid)
    else:
        form = StatusUpdateForm(instance=service)

    return render(request, 'amc/update_status.html', {'form': form, 'service': service})

from django.db.models import Q

from .models import (
    ACRequest, WaterPurifierRequest, ChimneyHobRequest, Customer
)

from django.utils.timezone import localtime, now
from datetime import timedelta


def service_search_results(request):
    query = request.GET.get('q', '')
    services = []

    if query:
        ac_results = ACRequest.objects.filter(
            Q(customer__user__name__icontains=query) |
            Q(customer__user__email__icontains=query) |
            Q(product_brand__icontains=query) |
            Q(ac_type__icontains=query) |
            Q(comprensive__icontains=query) |
            Q(status__icontains=query)
        )

        purifier_results = WaterPurifierRequest.objects.filter(
            Q(customer__user__name__icontains=query) |
            Q(customer__user__email__icontains=query) |
            Q(product_brand__icontains=query) |
            Q(purifier_type__icontains=query) |
            Q(comprensive__icontains=query) |
            Q(status__icontains=query)
        )

        chimney_results = ChimneyHobRequest.objects.filter(
            Q(customer__user__name__icontains=query) |
            Q(customer__user__email__icontains=query) |
            Q(product_brand__icontains=query) |
            Q(device_type__icontains=query) |
            Q(comprensive__icontains=query) |
            Q(status__icontains=query)
        )

        services = list(ac_results) + list(purifier_results) + list(chimney_results)

        # Add category_slug and display_date to each service
        for req in services:
            if isinstance(req, ACRequest):
                req.category_slug = 'air-conditioner'
            elif isinstance(req, WaterPurifierRequest):
                req.category_slug = 'water-filter'
            elif isinstance(req, ChimneyHobRequest):
                req.category_slug = 'chimaney-hub'

            today = localtime(now()).date()
            created_date = localtime(req.created_at).date()
            if created_date == today:
                req.display_date = "Today"
            elif created_date == today - timedelta(days=1):
                req.display_date = "Yesterday"
            else:
                req.display_date = created_date.strftime("%d %b %Y")

    return render(request, 'amc/service_results.html', {'services': services})



#profile view

def profile_view(request):
    user = request.user
    return render(request, 'amc/profile.html', {'user': user})