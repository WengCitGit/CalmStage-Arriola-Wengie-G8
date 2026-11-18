from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('CalmStage Profile & Role', {
            'fields': ('role', 'contact_number', 'program_or_department', 'profile_photo')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('CalmStage Profile & Role', {
            'fields': ('email', 'first_name', 'last_name', 'role', 'contact_number')
        }),
    )