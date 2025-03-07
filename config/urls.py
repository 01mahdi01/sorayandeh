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
    path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('admin/', admin.site.urls),
    path('users/', include(("sorayandeh.users.urls", 'users'))),
    path('applicant/', include(("sorayandeh.applicant.urls", 'applicant'))),
    path('campaigns/', include(("sorayandeh.campaign.urls", 'campaigns'))),
    path('finance/', include(("sorayandeh.finance.urls", 'finance'))),
    path("bankgateways/", az_bank_gateways_urls()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
