from django.urls import path

from .apis import *

urlpatterns = [
    path('create_campaign/',CreateCampaign.as_view(),name='create_campaign'),
]
