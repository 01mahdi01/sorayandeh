from django.contrib import admin
from .models import Campaign, CampaignCategory, Participants


class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Show the title of the category in the list view
    search_fields = ('title',)  # Enable searching by title


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'school', 'created_date', 'is_active')  # Show relevant fields in the list view
    list_filter = ('category', 'school', 'is_active')  # Enable filtering by category, school, and active status
    search_fields = (
    'title', 'school__name')  # Enable searching by title and school name (assuming `name` is a field in `School`)
    filter_horizontal = ('participants',)  # To display the Many-to-Many relationship in a more user-friendly way
    readonly_fields = ('created_date',)  # Make the created_date field read-only

    # You could also add more fields to the form if you want to customize it more:
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'school', 'applicant_info', 'estimated_money', 'is_active', 'gallery','description','steel_needed_money')
        }),
        ('Important Dates', {
            'fields': ('created_date',),
            'classes': ('collapse',)  # Make this section collapsible
        }),
    )


class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'created_date', 'participation_type')  # Show relevant fields in the list view
    list_filter = ('campaign', 'user')  # Enable filtering by campaign and user
    search_fields = ('user__username', 'campaign__title')  # Enable searching by user username and campaign title


# Register the models with the admin site
admin.site.register(CampaignCategory, CampaignCategoryAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Participants, ParticipantsAdmin)
