from django.db import models
from sorayandeh.users.models import BaseUser
from .validators import JSONSchemaValidator,MY_JSON_FIELD_SCHEMA
from django.core.exceptions import ValidationError

class School (models.Model):
    school = models.OneToOneField(BaseUser, on_delete=models.CASCADE,related_name='school_user')
    postal_code = models.CharField(max_length=100)
    school_code_num = models.CharField(max_length=100,unique=True)
    creator_employee_info = models.JSONField()
    address = models.TextField()
    requests_count = models.IntegerField(default=0)
    is_authenticated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Dynamically apply the validator before saving.
        Ensure that creator_employee_info field is validated against the schema.
        """
        # Validate the creator_employee_info JSON field against the schema
        json_validator = JSONSchemaValidator(limit_value=MY_JSON_FIELD_SCHEMA)
        json_validator(self.creator_employee_info)


    def __str__(self):
        return self.school_code_num



