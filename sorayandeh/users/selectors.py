from .models import Profile, BaseUser

def get_profile(user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)

def get_user(user_id:str)-> BaseUser:
    return BaseUser.objects.get(id=user_id)
