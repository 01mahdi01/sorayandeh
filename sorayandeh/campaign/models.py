from django.db import models
from sorayandeh.applicant.models import School
from sorayandeh.users.models import BaseUser


class CampaignCategory(models.Model):
    title = models.CharField(max_length=100)


class Campaign(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(CampaignCategory, related_name='campaign_categories')
    title = models.CharField(max_length=100)
    requests = models.JSONField()  # a list of needs
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    applicant_info = models.JSONField()   # name and the position of the actual person
    participants = models.ManyToManyField(BaseUser,through='Participants',related_name='campaigns_participated')
    preview_image = models.ImageField()
    video_link = models.URLField(verbose_name="Video Link",null=True, blank=True)




class Participants(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    participation_type = models.JSONField(verbose_name="Participation Type")