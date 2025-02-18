from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BaseUser, Profile, Person, Company

@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'phone', 'roll', 'is_admin', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('email', 'phone', 'name')
    list_filter = ('is_admin', 'is_deleted', 'roll', 'created_at')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Info', {
            'fields': ('email', 'name', 'phone', 'roll', 'password')
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_deleted', 'groups', 'user_permissions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'roll', 'password1', 'password2'),
        }),
    )

    ordering = ('-created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaigns_participated_count')
    search_fields = ('user__email', 'user__phone', 'user__name')
    readonly_fields = ('campaigns_participated_count',)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('base_user', 'national_code')
    search_fields = ('base_user__email', 'base_user__phone', 'base_user__name', 'national_code')
    list_filter = ('base_user__is_admin',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('base_user', 'employee_name', 'employee_position', 'company_registration_number')
    search_fields = ('base_user__email', 'base_user__phone', 'base_user__name', 'company_registration_number')

