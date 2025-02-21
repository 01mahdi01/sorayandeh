from django.db import models
from sorayandeh.applicant.models import School
from sorayandeh.users.models import BaseUser


class RequestCategory(models.Model):
    title = models.CharField(max_length=100)


class Campaign(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    applicant_info = models.JSONField()   # name and the position of the actual person
    participants = models.ManyToManyField(BaseUser,through='Participants',related_name='campaigns_participated')
    preview_image = models.ImageField(upload_to='preview_images/')
    video_link = models.URLField(verbose_name="Video Link",null=True, blank=True)
    estimated_money = models.IntegerField(verbose_name="Estimated Money", default=0)
    is_active = models.BooleanField(default=True)




class Participants(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='participants_list')
    participation_type = models.JSONField(verbose_name="Participation Type")

class Requests(models.Model):
    name= models.CharField(max_length=100)
    campaign= models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='requests_list')
    category = models.ForeignKey(RequestCategory, related_name='request_categories',on_delete=models.CASCADE)
    #---------------------------------------------need to be talked about
