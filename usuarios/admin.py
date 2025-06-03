from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add 'role' to fieldsets for easy editing in admin
    # Copying existing fieldsets and adding role
    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Role', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'role']


admin.site.register(CustomUser, CustomUserAdmin)
