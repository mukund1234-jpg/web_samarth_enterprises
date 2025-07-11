from django.contrib import admin

from .models import (
    ProductCategory,
    Customer,
    ACRequest,
    WaterPurifierRequest,
    ChimneyHobRequest,
)

# Inline read-only User email display for Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user', 'phone', 'created_by')

    def get_full_name(self, obj):
        return obj.user.name or obj.user.email
    get_full_name.short_description = 'Customer Name'

# Product Category
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Common admin display for all requests
class BaseRequestAdmin(admin.ModelAdmin):
    list_display = (
        'uuid','customer_email', 'category', 'status', 'comprensive', 'price', 'created_at', 'added_by'
    )
    list_filter = ('status', 'comprensive', 'category', 'created_at')
    search_fields = ('customer__user__email', 'category__name')
    readonly_fields = ('price', 'created_at')
    ordering = ('-created_at',)

    def customer_email(self, obj):
        return obj.customer.user.email if obj.customer and obj.customer.user else 'N/A'
    customer_email.short_description = 'Customer Email'

    def added_by(self, obj):
        # ✅ Show the name of the office worker who created the customer
        if obj.customer and obj.customer.created_by:
            return obj.customer.created_by.name or obj.customer.created_by.email
        return 'N/A'
    added_by.short_description = 'Added By (Office Worker Name)'



# AC Request Admin
@admin.register(ACRequest)
class ACRequestAdmin(BaseRequestAdmin):
    list_display = BaseRequestAdmin.list_display + ('ac_type', 'product_brand', 'amc_years', 'visit_count')
    list_filter = BaseRequestAdmin.list_filter + ('ac_type', 'product_brand', 'amc_years')

# Water Purifier Request Admin
@admin.register(WaterPurifierRequest)
class WaterPurifierRequestAdmin(BaseRequestAdmin):
    list_display = BaseRequestAdmin.list_display + ('purifier_type', 'product_brand', 'amc_years', 'visit_count')
    list_filter = BaseRequestAdmin.list_filter + ('product_brand',)

# Chimney Hob Request Admin
@admin.register(ChimneyHobRequest)
class ChimneyHobRequestAdmin(BaseRequestAdmin):
    list_display = BaseRequestAdmin.list_display + ('device_type', 'product_brand', 'amc_years', 'visit_count')
    list_filter = BaseRequestAdmin.list_filter + ('device_type', 'product_brand',)
