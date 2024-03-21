from django.db import models

from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    address = models.TextField()
    is_registered = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    search_fields = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
