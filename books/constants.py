from django.db import models

MAX_NAME_LENGTH: int = 150
MAX_NUMBER_ISBN: int = 13
MAX_AGE_RATING_LENGTH: int = 14
MAX_STATUS_LENGTH: int = 9


class AgeRating(models.TextChoices):
    ABOVE_ZERO = ("ABOVE_ZERO", "0+")
    ABOVE_SIX = ("ABOVE_SIX", "6+")
    ABOVE_TWELVE = ("ABOVE_TWELVE", "12+")
    ABOVE_SIXTEEN = ("ABOVE_SIXTEEN", "16+")
    ABOVE_EIGHTEEN = ("ABOVE_EIGHTEEN", "18+")


class Status(models.TextChoices):
    AVAILABLE = ("AVAILABLE", "Доступна")
    BUSY = ("BUSY", "Занята")
    RESERVED = ("RESERVED", "Зарезервирована")
