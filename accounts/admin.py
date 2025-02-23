from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Adds user sql table to Django admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'password', 'role', 'verified']
    list_editable = ('role', 'verified')  # Admin can edit roles from the list view
    list_filter = ('role', 'verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'verified')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

