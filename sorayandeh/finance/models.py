from django.db import models
from sorayandeh.users.models import BaseUser
from sorayandeh.campaign.models import Campaign
from azbankgateways.models import Bank


class FinancialLogs(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    tracing_code = models.CharField(max_length=100)
    transaction = models.ForeignKey(Bank, on_delete=models.CASCADE)
