from celery.beat import info
from django.db import transaction
from .models import BaseUser, Profile, Person, Company
from rest_framework.generics import get_object_or_404
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db import DatabaseError
from rest_framework_simplejwt.tokens import RefreshToken

def update_profile(*, user: BaseUser, **fields) -> Profile:
    """
    Update a profile for the given user with provided fields.

    Args:
        user (BaseUser): The user instance associated with the profile.
        **fields: Arbitrary fields to update on the profile.

    Returns:
        Profile: The updated Profile instance.
    """
    Profile.objects.filter(user=user).update(**fields)
    return Profile.objects.get(user=user)


def create_user(*, email: str, password: str, phone, name: str, roll: str) -> BaseUser:
    """
        Creates a new BaseUser with the provided information.

        Args:
            email (str): User's email address.
            password (str): User's password.
            info (dict): Additional user information (JSON format).
            phone (str): User's phone number.
            name (str): User's name.
            is_company (bool): Indicates if the user is a company.

        Returns:
            BaseUser: The created BaseUser instance.
        """
    return BaseUser.objects.create_user(email=email, password=password, phone=phone, name=name,
                                        roll=roll)


@transaction.atomic
def register(*, email: str, password: str, info, phone,
             name, roll: str) -> BaseUser:
    """
    Registers a new user and creates a profile for the user.

    Args:
        email (str): User's email address.
        password (str): User's password.
        info (dict): Additional user information (JSON format).
        phone (str): User's phone number.
        name (str): User's name.
        is_company (bool): Indicates if the user is a company.

    Returns:
        BaseUser: The created BaseUser instance.
    """
    print("*"*20,info)
    user = create_user(email=email, password=password, phone=phone, name=name, roll=roll)
    Profile.objects.create(user=user)
    if roll == 'co':
        try:
            employee_name = info.get('employee_name')
            employee_position = info.get('employee_position')
            company_registration_number = info.get('company_registration_number')
            Company.objects.create(base_user=user, employee_name=employee_name, employee_position=employee_position,
                               company_registration_number=company_registration_number)
        except Exception as e:
            print(e)
    if roll == "pe":
        try:
            national_code = info.get('national_code')
            Person.objects.create(base_user=user, national_code=national_code)
        except Exception as e:
            print(e)

    return user

@transaction.atomic
def update_user(user_id, **fields):
    """
    Updates the user's information with only the fields provided.

    Args:
        user_id (int): ID of the user to update.
        **fields: Keyword arguments for fields to update, such as:
            - name (str): New name for the user.
            - phone (str): New phone number for the user.
            - email (str): New email for the user.
            - info (dict): Updated additional user information (JSON format).

    Returns:
        BaseUser: The updated BaseUser instance.
    """
    # Fetch user instance

    user = get_object_or_404(BaseUser, id=user_id)
    if user.roll in ["co","pe"]:
        info = fields.get("info", {})

        # Handle 'roll' changes
        # new_roll = fields.get("roll")
        # if new_roll and new_roll != user.roll:
        #     if user.roll == "co":
        #         Company.objects.filter(base_user=user).delete()
        #         Person.objects.create(base_user=user, national_code=info.get("national_code"))
        #     elif user.roll == "pe":
        #         Person.objects.filter(base_user=user).delete()
        #         Company.objects.create(
        #             base_user=user,
        #             employee_name=info.get("employee_name"),
        #             employee_position=info.get("employee_position"),
        #             company_registration_number=info.get("company_registration_number"),
        #         )
        #     user.roll = new_roll  # Update roll

        # Update related model fields
        if user.roll == "pe":
            person_data = {}
            if "national_code" in info:
                person_data["national_code"] = info["national_code"]

            if person_data:  # Only update if data is present
                Person.objects.update_or_create(base_user=user, defaults=person_data)

        elif user.roll == "co":
            company_data = {}
            for field in ["employee_name", "employee_position", "company_registration_number"]:
                if field in info:
                    company_data[field] = info[field]

            if company_data:  # Only update if data is present
                Company.objects.update_or_create(base_user=user, defaults=company_data)

        # Update user model fields
        user_fields = {key: value for key, value in fields.items() if hasattr(user, key)}
        for field, value in user_fields.items():
            setattr(user, field, value)

        user.save()  # Save changes to the user

        return {"success": True, "user":user }
    else:
        return {"success": False, "error": 'you are an school'}

@transaction.atomic
def update_password(user_id, password, old_password):
    """
    Updates the user's password and expires their active sessions.

    Args:
        user_id (int): ID of the user to update.
        password (str): New password for the user.
        old_password (str): Current password for verification.

    Returns:
        dict: Success or error message.
    """
    user = get_object_or_404(BaseUser, id=user_id)

    # ❌ Fix: Stop function execution if the old password is incorrect
    if not user.check_password(old_password):
        return {"success": False, "error": "Wrong old password"}

    try:
        # 🔹 Log out from all active sessions
        # user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        # for session in user_sessions:
        #     data = session.get_decoded()
        #     if str(user.id) == data.get('_auth_user_id'):
        #         session.delete()

        # 🔹 Set the new password
        user.set_password(password)
        user.save()

        # # 🔹 Remove refresh tokens (so user must log in again)
        # RefreshToken.for_user(user)

        return {"success": True, "message": "Password updated successfully"}

    except DatabaseError as e:
        return {"success": False, "error": "Error updating password: " + str(e)}


def delete_user(user_id):
    try:
        Profile.objects.filter(user=user_id).delete()
        user = BaseUser.objects.get(id=user_id).update(is_deleted=True)
        return {"success": True, "object": user}
    except DatabaseError as e:
        return {"success": False, "error": "database error occurred: " + str(e)}

# def delete_profile(user_id):
#     Profile.objects.filter(user=user_id).delete()
