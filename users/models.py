import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .constants import (
    MAX_COUNTRY_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_CODE_LENGTH,
    TOKEN_EXPIRES_MINUTES,
    Roles
)
from .validators import (
    KirillicLettersValidator,
    EmailValidator,
    PhoneNumberValidator
)


class Country(models.Model):
    name = models.CharField(max_length=MAX_COUNTRY_LENGTH, unique=True)
    code = models.CharField(max_length=MAX_CODE_LENGTH, unique=True)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ("name",)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(
        "Имя",
        max_length=MAX_NAME_LENGTH,
        validators=[KirillicLettersValidator()],
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=MAX_NAME_LENGTH,
        validators=[KirillicLettersValidator()],
    )
    email = models.EmailField(
        "Почта",
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        validators=[EmailValidator()]
    )
    phone_number = models.CharField(
        "Телефон",
        max_length=MAX_PHONE_LENGTH,
        unique=True,
        validators=[PhoneNumberValidator()],
        null=True,
        blank=True
    )
    age = models.CharField(
        "Возраст",
        max_length=MAX_CODE_LENGTH,
        null=True,
        blank=True

    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    role = models.CharField(
        "Роль",
        choices=Roles.choices,
        max_length=MAX_COUNTRY_LENGTH,
        default=Roles.USER
    )
    is_blocked = models.BooleanField("Заблокирован", default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.username


class ActivationToken(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    token = models.UUIDField(
        "Токен активации",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )
    expires_at = models.DateTimeField(
        "Истекает",
    )

    def token_is_valid(self):
        return self.expires_at > timezone.now()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(
                minutes=TOKEN_EXPIRES_MINUTES,
            )

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.token}"
