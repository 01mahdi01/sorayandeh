from django.contrib.auth.backends import BaseBackend
from .models import School

class SchoolAuthenticationBackend(BaseBackend):
    def authenticate(self, request, school_code_num=None, password=None, **kwargs):
        if not school_code_num:
            return None
        try:
            school = School.objects.get(school_code_num=school_code_num)
            base_user = school.school
            if base_user and base_user.check_password(password):
                return base_user
        except School.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return School.objects.get(school__id=user_id).school
        except School.DoesNotExist:
            return None
