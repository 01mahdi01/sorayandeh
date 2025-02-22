from django.urls import path

from .apis import *

urlpatterns = [
    path('create_campaign/',CreateCampaign.as_view(),name='create_campaign'),
    path('contribute/',ContributeCampaign.as_view(),name='contribute'),
    path('campaign_list/',CampaignList.as_view(),name='campaign_list'),
]
