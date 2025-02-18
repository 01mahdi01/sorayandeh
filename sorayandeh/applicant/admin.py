from django.contrib import admin
from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school', 'school_code_num', 'postal_code', 'is_authenticated', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('school_code_num', 'postal_code', 'school__email')  # Assuming BaseUser has an email field
    list_filter = ('is_authenticated', 'is_deleted', 'created_at')

    readonly_fields = ('created_at', 'updated_at')  # These fields should not be editable

    fieldsets = (
        ('Basic Info', {
            'fields': ('school', 'postal_code', 'school_code_num', 'creator_employee_info', 'address')
        }),
        ('Status', {
            'fields': ('is_authenticated', 'is_deleted', 'requests_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
