import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .constants import (
    MAX_COUNTRY_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_CODE_LENGTH,
    TOKEN_EXPIRES_MINUTES,
    EMAIL_ALLOWED_DOMAINS_RE,
    PHONE_NUMBER_RE,
    Roles
)
from .validators import (
    UserFirstNameAndLastNameValidator
)


class Country(models.Model):
    name = models.CharField(max_length=MAX_COUNTRY_LENGTH, unique=True)
    code = models.CharField(max_length=MAX_CODE_LENGTH, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(
        "Имя",
        max_length=MAX_NAME_LENGTH,
        validators=[UserFirstNameAndLastNameValidator()],
        help_text="Имя пользователя может содержать только русские буквы"
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=MAX_NAME_LENGTH,
        validators=[UserFirstNameAndLastNameValidator()],
        help_text="Фамилия пользователя может содержать только русские буквы"
    )
    email = models.EmailField(
        "Почта",
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        validators=[RegexValidator(
            EMAIL_ALLOWED_DOMAINS_RE,
            "Разрешены только почтовые домены: gmail.com, yandex.ru, ya.ru, mail.ru, yahoo.com, outlook.com"
        )]
    )
    phone_number = models.CharField(
        "Телефон",
        max_length=MAX_PHONE_LENGTH,
        unique=True,
        validators=[RegexValidator(
            PHONE_NUMBER_RE,
            "Неправильный формат номера"
        )],
        help_text="Номер телефона начинается с +7 или 8, далее - код оператора 3 цифры, его допускается брать в "
                  "скобки, далее - 7 цифр группами: 3 цифры, 2 цифры, 2 цифры, слитно или с использованием скобок, "
                  "дефисов и пробелов. Допускается весь номер указывать слитно.",
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
        null=True)
    is_blocked = models.BooleanField("Заблокирован", default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}".rstrip()

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
