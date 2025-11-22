from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    MAX_COUNTRY_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    # TOKEN_EXPIRES_MINUTES,
)


class User(AbstractUser):
    first_name = models.CharField(
        "Имя", max_length=MAX_NAME_LENGTH, blank=True
    )
    last_name = models.CharField(
        "Имя", max_length=MAX_NAME_LENGTH, blank=True
    )
    email = models.EmailField(
        "Почта", max_length=MAX_EMAIL_LENGTH, unique=True
    )
    phone_number = models.CharField(
        "Телефон",
        max_length=MAX_PHONE_LENGTH,
        blank=True,
    )
    country = models.CharField(
        "Страна", max_length=MAX_COUNTRY_LENGTH, blank=True
    )
    is_blocked = models.BooleanField("Заблокирован", default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
