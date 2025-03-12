from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("api/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('api/admin/', admin.site.urls),
    path('api/users/', include(("sorayandeh.users.urls", 'users'))),
    path('api/applicant/', include(("sorayandeh.applicant.urls", 'applicant'))),
    path('api/campaigns/', include(("sorayandeh.campaign.urls", 'campaigns'))),
    path('api/finance/', include(("sorayandeh.finance.urls", 'finance'))),
    path("api/bankgateways/", az_bank_gateways_urls()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)