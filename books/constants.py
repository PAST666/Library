from django.db import models

MAX_NAME_LENGTH: int = 150
MAX_PAGES_COUNT_LENGTH: int = 4
MAX_PUBLICATION_YEAR_LENGTH: int = 4
MAX_NUMBER_ISBN: int = 13
MAX_AGE_RATING_LENGTH: int = 3


class Genre(models.TextChoices):
    FANTASY = ("FANTASY", "Фантастика")
    THRILLER = ("THRILLER", "Триллер")
    HORROR = ("HORROR", "Ужас")
    ADVENTURE = ("ADVENTURE", "Приключения")
    FICTION = ("FICTION", "Художественная литература")
    ROMAN = ("ROMAN", "Роман")


class AgeRating(models.TextChoices):
    ABOVE_ZERO = ("ABOVE_ZERO", "0+")
    ABOVE_SIX = ("ABOVE_SIX", "6+")
    ABOVE_TWELVE = ("ABOVE_TWELVE", "12+")
    ABOVE_SIXTEEN = ("ABOVE_SIXTEEN", "16+")
    ABOVE_EIGHTEEN = ("ABOVE_EIGHTEEN", "18+")
