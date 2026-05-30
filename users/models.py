import uuid
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from core.validators import (
    EmailValidator,
    KirillicLettersValidator,
    PhoneNumberValidator,
)

from .constants import (
    MAX_CODE_LENGTH,
    MAX_COUNTRY_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    Roles,
)
from .managers import ActivationTokenManager, UserManager


class Country(models.Model):
    name = models.CharField(verbose_name="Название страны", max_length=MAX_COUNTRY_LENGTH, unique=True)
    code = models.CharField(
        verbose_name="Буквенный код страны",
        max_length=MAX_CODE_LENGTH, unique=True,
        validators=[MinLengthValidator(2)]
    )

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
    birth_date = models.DateField(
        "Дата рождения",
        blank=False,
        null=False
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
    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    @property
    def age(self) -> int | None:
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    @property
    def is_admin(self) -> bool:
        return self.role == Roles.ADMIN

    @property
    def is_moderator(self) -> bool:
        return self.role == Roles.MODERATOR

    @property
    def is_editor(self) -> bool:
        return self.role == Roles.EDITOR

    @property
    def is_librarian(self) -> bool:
        return self.role == Roles.LIBRARIAN

    @property
    def is_user(self) -> bool:
        return self.role == Roles.USER

    @property
    def is_vip(self) -> bool:
        return self.role == Roles.VIP

    def __str__(self):
        return self.username


class ActivationToken(models.Model):

    user = models.OneToOneField(
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
    objects = ActivationTokenManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(expires_at__gt=timezone.now()),
                name="unique_active_token",
            )
        ]
        verbose_name = "Токен активации"
        verbose_name_plural = "Токены активации"
        ordering = ("user",)

    @property
    def is_valid(self) -> bool:
        return self.expires_at > timezone.now()

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.token}"
