from django.db import models

MAX_NAME_LENGTH: int = 150
MAX_PAGES_COUNT_LENGTH: int = 3
MAX_PUBLICATION_YEAR_LENGTH: int = 4

class Genre(models.TextChoices):
    FANTASY = ("FANTASY", "Фантастика")
    THRILLER = ("THRILLER", "Триллер")
    HORROR = ("HORROR", "Ужас")
    ADVENTURE = ("ADVENTURE", "Приключения")
    FICTION = ("FICTION", "Художественная литература")
    ROMAN = ("ROMAN", "Роман")

