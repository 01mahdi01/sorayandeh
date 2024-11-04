from django.db import transaction
from .models import BaseUser, Profile
from sorayandeh.campaign.models import Campaign
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.utils import timezone


def create_profile(*, user: BaseUser, campaigns_participated_count: int, donations: dict | None) -> Profile:
    """
    Creates a profile for the given user.

    Args:
        user (BaseUser): The user instance associated with the profile.
        campaigns_participated_count (int): Number of campaigns the user has participated in.
        donations (dict, optional): Dictionary of donation details, if any.

    Returns:
        Profile: The created Profile instance.
    """
    return Profile.objects.create(user=user, donations=donations,
                                  campaigns_participated_count=campaigns_participated_count)


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
def register(*, campaigns_participated_count: int, donations: dict | None, email: str, password: str, info, phone,
             name, is_company: bool) -> BaseUser:
    """
    Registers a new user and creates a profile for the user.

    Args:
        campaigns_participated_count (int): Number of campaigns the user has participated in.
        donations (dict, optional): Dictionary of donation details, if any.
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
    # create_profile(user=user, donations=donations,campaigns_participated_count=campaigns_participated_count)

    return user


def update_user(user_id, name, phone, email, info):
    """
    Updates the user's information.

    Args:
        user_id (int): ID of the user to update.
        name (str): New name for the user.
        phone (str): New phone number for the user.
        email (str): New email for the user.
        info (dict): Updated additional user information (JSON format).

    Returns:
        BaseUser: The updated BaseUser instance.
    """
    user = get_object_or_404(BaseUser, id=user_id)
    user.name = name
    user.phone = phone
    user.email = email
    user.info = info
    user.save()
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
    user = get_object_or_404(BaseUser, id=user_id)
    # Log the user out of all active sessions
    user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in user_sessions:
        if str(user.id) == session.get_decoded().get('_auth_user_id'):
            session.delete()
    user.set_password(password)
    user.save()


# def sign_in(self, request):
#     phone_number = request.POST.get('phone_number', None)
#     password = request.POST.get('password', None)
#
#     if not phone_number:
#         messages.error(request, 'شماره تلفن نمیتواند خالی باشد')
#         return redirect('users:register')
#
#     if not password:
#         messages.error(request, 'پسورد نمیتواند خالی باشد')
#         return redirect('users:register')
#
#     user = User.objects.filter(phone_number=phone_number).first()
#     if user and user.check_password(password):
#         return user
#
#     messages.error(request,
#                    'نام کاربری یا پسورد اشتباه است! یا شما یک هکر دیوس هستید که میخواهید به سیستم ما نفوذ کنید کور خوندی دیوس امنیت جنگو بالاس🖕')
#     return redirect('users:register')
