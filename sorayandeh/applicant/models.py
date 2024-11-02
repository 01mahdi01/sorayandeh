from django.db import models

# Create your models here.
class School (models.Model):
    name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    school_code_num=models.CharField(max_length=100)
    applicant_count = models.IntegerField(default=0)
    def __str__(self):
        return self.name