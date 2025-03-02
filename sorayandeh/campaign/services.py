from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Campaign,Participants,CampaignCategory
from sorayandeh.applicant.models import School
import os
from django.core.files.storage import default_storage
import uuid
from sorayandeh.users.models import BaseUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

def create_campaign(user_id, **kwargs):
    campaign_category = CampaignCategory.objects.get(pk=kwargs['campaign_category'])
    school = BaseUser.objects.select_related('school_user').get(pk=user_id)
    preview_images = kwargs.get('preview_images')
    image_paths = []

    for image in preview_images:
        # Define the upload path
        new_name = f"{uuid.uuid4().hex}.png"  # Shortened filename without extra spaces
        upload_path = os.path.join("CA", new_name)
        file_path = default_storage.save(upload_path, image)

        # Store the relative path in the JSONField
        image_paths.append(file_path)

    # Remove preview_images from kwargs to prevent conflicts
    for key in ["preview_images", "campaign_category"]:
        kwargs.pop(key, None)
    steel_needed_money=kwargs.get('estimated_money')
    # Create the campaign
    campaign = Campaign.objects.create(category=campaign_category, school=school.school_user, gallery=image_paths,steel_needed_money=steel_needed_money, **kwargs)


    return campaign

@transaction.atomic
def contribute(user_id, campaign_id,participation_type):
    # we must first verify the contribution from the Finance
    #
    #
    user=BaseUser.objects.get(pk=user_id)
    campaign = get_object_or_404(Campaign.objects.select_for_update(), pk=campaign_id)
    contributed = Participants.objects.create(user=user,campaign=campaign,participation_type=participation_type)
    campaign.participants.add(user)
    campaign.save()
    print(campaign.participants.all())
    return contributed




def campaign_list(request):
    # Get all campaigns
    campaigns = Campaign.objects.all()

    # Get the page number from the request, default to 1
    page_number = request.GET.get('page', 1)

    # Create a Paginator object with 10 items per page
    paginator = Paginator(campaigns, 10)

    try:
        # Get the page based on the page_number
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If the page is not an integer, return the first page
        page = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, return the last page
        page = paginator.page(paginator.num_pages)

    # Prepare the response data
    campaign_data = []
    for campaign in page:
        campaign_data.append({
            "id": campaign.id,
            "title": campaign.title,
            "created_date": campaign.created_date,
            "estimated_money": campaign.estimated_money,
            "is_active": campaign.is_active,
        })

    # Return the paginated campaigns in JSON format
    return JsonResponse({
        'campaigns': campaign_data,
        'total_pages': paginator.num_pages,
        'current_page': page.number,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
    })