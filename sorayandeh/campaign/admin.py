from django.contrib import admin
from .models import Campaign, CampaignCategory, Participants


class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class ParticipantsInline(admin.TabularInline):  # Inline admin for Participants model
    model = Participants
    extra = 1  # Shows 1 empty form for adding new participants
    autocomplete_fields = ['user']  # Helps in selecting users efficiently


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'school', 'created_date', 'is_active')
    list_filter = ('category', 'school', 'is_active')
    search_fields = ('title', 'school__name')
    readonly_fields = ('created_date',)
    inlines = [ParticipantsInline]  # Use an inline admin instead of filter_horizontal

    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'school', 'applicant_info', 'estimated_money', 'is_active', 'gallery', 'description', 'steel_needed_money')
        }),
        ('Important Dates', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )


class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'created_date', 'participation_type')
    list_filter = ('campaign', 'user')
    search_fields = ('user__username', 'campaign__title')


# Register the models with the admin site
admin.site.register(CampaignCategory, CampaignCategoryAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Participants, ParticipantsAdmin)
