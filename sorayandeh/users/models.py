from django.db import models
from sorayandeh.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin


class BaseUserManager(BUM):
    def create_user(self, email, roll, name, phone, is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_admin=is_admin, name=name, phone=phone,
                          roll=roll)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self,phone, email, password=None):
        user = self.model(
            email=email,
            phone=phone,
            roll="admin",
            is_admin=True,
        )
        user.set_password(password)

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    ROLL_CHOICES = [
        ("pe", "person"),
        ("co", "company"),
        ("ap", "applicant"),
    ]
    email = models.EmailField(verbose_name="email address",
                              unique=True)
    name = models.CharField(verbose_name="Name", max_length=100)
    phone = models.CharField(verbose_name="Phone number", max_length=20, unique=True)
    # info = models.JSONField(
    #     verbose_name="Info")  # if it is a company or a person///// its schema is defined in the api serializers
    # is_company = models.BooleanField()
    roll = models.CharField(verbose_name="Roll number", max_length=20, choices=ROLL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    donations = models.JSONField(verbose_name="Donations", default=dict)
    campaigns_participated_count = models.PositiveIntegerField(default=0)


class Person(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    national_code = models.CharField(max_length=100, unique=True)


class Company(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=100)
    employee_position = models.CharField(max_length=100)
    company_registration_number = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name
