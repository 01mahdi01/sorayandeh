from .models import Campaign,Participants,CampaignCategory
from sorayandeh.applicant.models import School
import os
from django.core.files.storage import default_storage
import uuid
from sorayandeh.users.models import BaseUser


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

    # Create the campaign
    campaign = Campaign.objects.create(category=campaign_category, school=school.school_user, gallery=image_paths, **kwargs)


    return campaign


def contribute():
    pass



