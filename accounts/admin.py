from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, OTP
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email','name' ,'role', 'is_active', 'is_staff']
    search_fields = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('role','name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','role', 'password1', 'password2'),
        }),
    )

    # Use email as username
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)
