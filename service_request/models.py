from django.db import models
from django.conf import settings
from datetime import timedelta, date
from django.utils.text import slugify
from baseModel.base import *
User = settings.AUTH_USER_MODEL


AC_BRAND_CHOICES = [
    ('Voltas', 'Voltas'),
    ('LG', 'LG'),
    ('Daikin', 'Daikin'),
    ('Samsung', 'Samsung'),
    ('Hitachi', 'Hitachi'),
]

WATER_PURIFIER_BRANDS = [
    ('Kent', 'Kent'),
    ('Aquaguard', 'Aquaguard'),
    ('Pureit', 'Pureit'),
    ('Livpure', 'Livpure'),
    ('Blue Star', 'Blue Star'),
]

CHIMNEY_HOB_BRANDS = [
    ('Elica', 'Elica'),
    ('Faber', 'Faber'),
    ('Hindware', 'Hindware'),
    ('Glen', 'Glen'),
    ('Bosch', 'Bosch'),
]
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, unique=True)  # temporarily allow null

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name.lower())
            unique_slug = base_slug
            num = 1
            while ProductCategory.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_customers')

    def __str__(self):
        return self.user.name or self.user.email

    


class RequestForm(BaseModel):  # Inherit here
    STATUS_CHOICES = [('Pending', 'Pending'), ('Completed', 'Completed')]
    COM_CHOICES = [('Comprensive', 'Comprensive'), ('Non-Comprensive', 'Non-Comprensive')]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    bill = models.FileField(upload_to='bills/', blank=True, null=True)
    comprensive = models.CharField(max_length=20, choices=COM_CHOICES, default='Comprensive')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    price = models.PositiveIntegerField(default=0) 
    third_party_worker_name = models.CharField(max_length=100, blank=True, null=True)
    visit_count = models.PositiveIntegerField(null=True , blank= True)
    payment_method = models.CharField(
        max_length=20,
        choices=[('Cash', 'Cash'), ('GPay', 'GPay'), ('Cheque', 'Cheque')],
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.start_date and hasattr(self, 'amc_years'):
            self.end_date = self.start_date + timedelta(days=365 * self.amc_years)
        super().save(*args, **kwargs)

class ACRequest(RequestForm):
    ac_type = models.CharField(max_length=50, choices=[('SAC', 'Split AC'), ('WAC', 'Window AC')])
    product_brand = models.CharField(max_length=100, choices=AC_BRAND_CHOICES)
    amc_years = models.PositiveIntegerField(choices=[(1, '1 Year'), (3, '3 Year')])


    def save(self, *args, **kwargs):
        base_price = 1000 if self.amc_years == 1 else 3000
        if self.comprensive == 'Comprensive':
            base_price += 300
        self.price = base_price

        # Set visit count
        if self.amc_years == 1:
            self.visit_count = 3
        elif self.amc_years == 3:
            self.visit_count = 9  # You mentioned 9 for 3 years

        super().save(*args, **kwargs)

        

class WaterPurifierRequest(RequestForm):
    purifier_type = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=100, choices=WATER_PURIFIER_BRANDS)
    amc_years = models.PositiveIntegerField(choices=[(1, '1 Year'), (3, '3 Year')])

    def save(self, *args, **kwargs):
        base_price = 1000 if self.amc_years == 1 else 3000
        if self.comprensive == 'Comprensive':
            base_price += 300
        self.price = base_price

        # Set visit count
        if self.amc_years == 1:
            self.visit_count = 3
        elif self.amc_years == 3:
            self.visit_count = 9  # You mentioned 9 for 3 years

        super().save(*args, **kwargs)


class ChimneyHobRequest(RequestForm):
    device_type = models.CharField(max_length=20, choices=[('Chimney', 'Chimney'), ('Hob+Chimney', 'Hob + Chimney')])
    product_brand = models.CharField(max_length=100, choices=CHIMNEY_HOB_BRANDS)
    amc_years = models.PositiveIntegerField(choices=[(1, '1 Year'), (3, '3 Year')])

    def save(self, *args, **kwargs):
        base_price = 1000 if self.amc_years == 1 else 3000
        if self.comprensive == 'Comprensive':
            base_price += 300
        self.price = base_price

        # Set visit count
        if self.amc_years == 1:
            self.visit_count = 3
        elif self.amc_years == 3:
            self.visit_count = 9  # You mentioned 9 for 3 years

        super().save(*args, **kwargs)

