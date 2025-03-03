from azbankgateways.views.banks import go_to_bank_gateway
from django.urls import path
from .apis import RequestPaymentUrl,CallbackPaymentUrl,GetFinancialLogs

urlpatterns = [

    path('get_bank_url/', RequestPaymentUrl.as_view(),name="get_bank_url"),
    path('callback_gateway/', CallbackPaymentUrl.as_view(),name="callback_gateway"),
    path('get_financial_logs/', GetFinancialLogs.as_view(),name="get_financial_logs"),


]
