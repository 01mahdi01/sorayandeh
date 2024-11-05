from django.db import transaction
from .models import BaseUser, Profile
from sorayandeh.campaign.models import Campaign
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.utils import timezone


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

def create_user(*, email: str, password: str, info, phone, name, is_company: bool) -> BaseUser:
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
    return BaseUser.objects.create_user(email=email, password=password, info=info, phone=phone, name=name,
                                        is_company=is_company)


@transaction.atomic
def register(*, email: str, password: str, info, phone,
             name, is_company: bool) -> BaseUser:
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
    user = create_user(email=email, password=password, info=info, phone=phone, name=name, is_company=is_company)
    Profile.objects.create(user=user)

    return user


def update_user(user_id, **fields) -> BaseUser:
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

    # Update only the provided fields
    for field, value in fields.items():
        if hasattr(user, field):  # Only update fields that exist on the model
            setattr(user, field, value)

    user.save()  # Save changes to the database
    return user

def update_password(user_id, password):
    """
    Updates the user's password and expires their active sessions.

    Args:
        user_id (int): ID of the user to update.
        password (str): New password for the user.

    Returns:
        None
    """
    print(user_id)
    user = get_object_or_404(BaseUser, id=user_id)
    # Log the user out of all active sessions
    user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in user_sessions:
        if str(user.id) == session.get_decoded().get('_auth_user_id'):
            session.delete()
    user.set_password(password)
    user.save()



def delete_user(user):
    pass


def delete_profile(user_id):
    Profile.objects.filter(user=user_id).delete()


