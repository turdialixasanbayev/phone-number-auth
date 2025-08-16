from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


admin.site.site_header = "phone-number-auth Admin Panel"
admin.site.site_title = "phone-number-auth Admin Panel"
admin.site.index_title = "Welcome to phone-number-auth Admin Panel"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    CustomUser Admin Interface
    """
    model = CustomUser
    ordering = ('phone_number',)
    search_fields = ('phone_number',)
    list_display = (
        'id',
        'phone_number',
        'status',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined'
    )
    readonly_fields = (
        'id',
        'last_login',
        'date_joined'
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'status'
    )
    fieldsets = (
        ('Login', {
            'fields': ('phone_number', 'password'),
            'classes': ('wide'),
        }),
        ("Permissions", {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'status'),
            'classes': ('wide'),
        }),
        ("Important Dates", {
            'fields': ('date_joined', 'last_login'),
            'classes': ('wide', 'collapse'),
        }),
        ("ID", {
            'fields': ('id',),
            'classes': ('wide', 'collapse'),
        }),
    )
    add_fieldsets = (
        ('Create Super User', {
            'fields': ('phone_number', 'password1', 'password2'),
            'classes': ('wide'),
        }),
        ("Permissions", {
            'fields': ('is_superuser', 'is_staff'),
            'classes': ('wide'),
        }),
    )
