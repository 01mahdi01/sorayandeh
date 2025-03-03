from django.contrib import admin
from .models import FinancialLogs

@admin.register(FinancialLogs)
class FinancialLogsAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'transaction')
    search_fields = ('user__username', 'campaign__name', 'transaction__tracking_code')
    list_filter = ('campaign',)

    def get_queryset(self, request):
        """Optimize queryset to avoid unnecessary queries."""
        return super().get_queryset(request).select_related('user', 'campaign', 'transaction')

