from django.urls import path

from .apis import *

urlpatterns = [
    path('test/',Test.as_view(),name='test'),
    path('create_campaign/',CreateCampaign.as_view(),name='create_campaign'),
]
