from django.db import models
from sorayandeh.users.models import BaseUser
from sorayandeh.campaign.models import Campaign

# Create your models here.
class FinancialLogs(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    tracing_code = models.CharField(max_length=100)
    transaction_date = models.DateTimeField()
    transaction_data = models.JSONField()