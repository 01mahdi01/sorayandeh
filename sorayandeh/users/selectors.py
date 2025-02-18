from .models import Profile, BaseUser

def get_profile(user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)


def get_user(user_id: str):
    json_data = {}
    base_user = BaseUser.objects.select_related("person", "company","school_user").get(pk=user_id)

    # Manually filter out non-serializable fields like '_state'
    base_user_data = {k: v for k, v in base_user.__dict__.items() if not k.startswith('_') if not k.__contains__("password") }
    json_data.update(base_user_data)

    if hasattr(base_user, "person"):
        person_data = {k: v for k, v in base_user.person.__dict__.items() if not k.startswith('_')}
        json_data.update(person_data)

    elif hasattr(base_user, "company"):
        company_data = {k: v for k, v in base_user.company.__dict__.items() if not k.startswith('_')}
        json_data.update(company_data)

    elif hasattr(base_user, "school_user"):
        school_user = {k: v for k, v in base_user.company.__dict__.items() if not k.startswith('_')}
        json_data.update(school_user)

    return json_data

