from django.db import models
from sorayandeh.users.models import BaseUser



class School (models.Model):
    school = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=100)
    school_code_num = models.CharField(max_length=100,unique=True)
    creator_employee_info = models.JSONField()
    address = models.TextField()
    requests_count = models.IntegerField(default=0)
    is_authenticated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    def __str__(self):
        return self.school_code_num



