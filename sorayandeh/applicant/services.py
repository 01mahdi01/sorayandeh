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

@transaction.atomic
def update_school(user_id, **kwargs):
    base_user = get_object_or_404(BaseUser.objects.select_related("school_user"), pk=user_id)
    school = base_user.school_user
    try:
        # Fetch BaseUser and related School object in one query


        # filtered_kwargs = {k: v for k, v in kwargs.items() if "school_code_num" not in k.lower()}

        # Update fields for BaseUser and School
        for field, value in kwargs.items():
            if hasattr(base_user, field):
                setattr(base_user, field, value)  # Update BaseUser fields
            elif hasattr(school, field):
                setattr(school, field, value)  # Update School fields

        # Validate and save both instances
        base_user.full_clean()
        base_user.save()
        base_user.school_user.save()

        return school  # Return updated School instance

    except (DatabaseError, ValidationError) as e:
        return {"error": str(e)}
