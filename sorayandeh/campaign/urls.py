from django.urls import path

from .apis import *

urlpatterns = [
    path('create_campaign/',CreateCampaign.as_view(),name='create_campaign'),
    path('contribute/',ContributeCampaign.as_view(),name='contribute'),
    path('campaign_list/',CampaignList.as_view(),name='campaign_list'),
    path('filter_by_category/',FilterByCategory.as_view(),name='filter_by_category'),
    path('singe_campaign/',GetSingleCampaign.as_view(),name='GetSingleCampaign'),
    path('get_categories/',GetCategories.as_view(),name='get_categories'),

]
