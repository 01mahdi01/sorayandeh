from django.shortcuts import get_object_or_404
from sorayandeh.applicant.models import School
from django.db import DatabaseError
from sorayandeh.users.services import create_user


def register_school(creator_employee_info, postal_code, school_code_num, name, phone, email, password) -> School:
    school_user = create_user(email=email, password=password, phone=phone, name=name, roll="ap")
    return School.objects.create(school=school_user, creator_employee_info=creator_employee_info,
                                 postal_code=postal_code, school_code_num=school_code_num)


def delete_school(school_id):
    return School.objects.filter(id=school_id).update(is_deleted=True)


def update_school(school_code, **kwargs):
    try:
        school = get_object_or_404(School, school_code_num=school_code)
        for field, value in kwargs.items():
            if hasattr(school, field):  # Only update fields that exist on the model
                setattr(school, field, value)
        school.save()
        return school
    except DatabaseError as er:
        return {"error": "database error occurred: " + str(er)}
