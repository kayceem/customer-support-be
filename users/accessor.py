from .models import User


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class UserAccessor:

    @staticmethod
    def get_user(**kwargs):
        return get_or_none(User, **kwargs)

    @staticmethod
    def create_user(email, name):
        return User.objects.create(email=email, first_name=name, username=email)
