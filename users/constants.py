from django.db import models

MAX_NAME_LENGTH: int = 150
MAX_PHONE_LENGTH: int = 12
MAX_EMAIL_LENGTH: int = 150
TOKEN_EXPIRES_MINUTES: int = 15
MAX_COUNTRY_LENGTH: int = 20
MAX_CODE_LENGTH: int = 2


class Roles(models.TextChoices):
    ADMIN = ("ADMIN", "Администратор")
    MODERATOR = ("MODERATOR", "Модератор")
    EDITOR = ("EDITOR", "Редактор")
    LIBRARIAN = ("LIBRARIAN", "Библиотекарь")
    USER = ("USER", "Пользователь")
    VIP = ("VIP", "VIP")
