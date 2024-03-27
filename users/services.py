from .accessor import UserAccessor
from rest_framework_simplejwt.tokens import RefreshToken


class User:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def create_user(email, name):
        return UserAccessor.create_user(email, name)

    @staticmethod
    def get_user_by_email(email):
        return UserAccessor.get_user(email=email)

    def __generate_auth_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    @classmethod
    def login(cls, email, name):
        user = cls.get_user_by_email(email)
        if not user:
            user = cls.create_user(email, name)
        return cls(user).__generate_auth_token()