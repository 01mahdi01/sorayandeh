from django.shortcuts import get_object_or_404
from sorayandeh.applicant.models import School
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from sorayandeh.users.models import BaseUser
from sorayandeh.users.services import create_user,update_user
from django.db import transaction

@transaction.atomic
def register_school(creator_employee_info, postal_code, school_code_num, name, phone, email, password,address) -> School:
    # First, create the School instance (without saving yet)
    school = School(
        creator_employee_info=creator_employee_info,
        postal_code=postal_code,
        school_code_num=school_code_num,
        address=address
    )
#-------------------------------need to change the logic
    # Perform validation before creating the user
    school.full_clean(exclude=['school'])  # This will call the clean() method and validate the creator_employee_info field
    #--------------------------------------- implement the registration  here
    # Create the user after validation passes
    school_user = create_user(email=email, password=password, phone=phone, name=name, roll="ap")

    # Now associate the validated user with the school and save the school
    school.school = school_user
    school.save()

    return school


def delete_school(school_id):
    return School.objects.filter(id=school_id).update(is_deleted=True)


def update_school(school_code, **kwargs):
    try:
        # Fetch the School instance
        school = get_object_or_404(School, school_code_num=school_code)

        # Update School fields
        school_fields_to_update = {}
        user_fields_to_update = {}

        for field, value in kwargs.items():
            if hasattr(school, field):  # Update School-specific fields
                setattr(school, field, value)
                school_fields_to_update[field] = value
            elif hasattr(school.school, field):  # Prepare fields for User update
                user_fields_to_update[field] = value

        # Validate and save the School instance
        school.full_clean()
        school.save()

        # Update the User (BaseUser) instance
        if user_fields_to_update:
            update_user(school.school.id, **user_fields_to_update)

        return school
    except DatabaseError as er:
        return {"error": f"Database error occurred: {str(er)}"}
    except ValidationError as ve:
        return {"error": f"Validation error: {str(ve)}"}
