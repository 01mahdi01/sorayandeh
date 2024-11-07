from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from sorayandeh.common.models import BaseModel

# Create your models here.
class SchoolManager(BUM):
    def create_school(self, postal_code, school_code_num, requests_count, name,password):
        if not school_code_num:
            raise ValueError("Users must have an code")

        school = self.model(name=name,postal_code=postal_code,school_code_num=school_code_num,requests_count=requests_count)

        if password is not None:
            school.set_password(password)
        else:
            school.set_unusable_password()

        school.full_clean()
        school.save(using=self._db)

        return school


class School (BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    school_code_num = models.CharField(max_length=100,unique=True)
    # creator_info = models.JSONField()
    requests_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    objects = SchoolManager()

    USERNAME_FIELD = 'school_code_num'  # Set unique identifier for authentication
    REQUIRED_FIELDS = ['name']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='school_groups',  # Custom related_name to avoid clash
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='school_user_permissions',  # Custom related_name to avoid clash
        blank=True
    )


    def __str__(self):
        return self.name


    def has_module_perms(self, app_label):
        return True

