from django.db import models

from .constants import (
    MAX_NAME_LENGTH,
    MAX_PAGES_COUNT_LENGTH,
    MAX_PUBLICATION_YEAR_LENGTH,
    MAX_NUMBER_ISBN,
    MAX_AGE_RATING_LENGTH,
    Genre,
    AgeRating
)

from .managers import BookManager

from users.models import User


class Book(models.Model):
    title: str = models.CharField(
        "Книга",
        max_length=MAX_NAME_LENGTH,
    )
    pages: int = models.IntegerField(
        "Количество страниц",
        max_length=MAX_PAGES_COUNT_LENGTH,
    )
    publication_year: int = models.IntegerField(
        "Год издания",
        max_length=MAX_PUBLICATION_YEAR_LENGTH,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
    )
    genre: str = models.CharField(
        "Жанр",
        choices=Genre.choices,
        max_length=MAX_NAME_LENGTH
    )
    isbn: str = models.CharField(
        "ISBN",
        max_length=MAX_NUMBER_ISBN
    )
    age_rating: str = models.CharField(
        "Возрастной рейтинг",
        choices=AgeRating.choices,
        max_length=MAX_AGE_RATING_LENGTH
    )
    is_taken: bool = models.BooleanField("Выдана", default=False)
    objects = BookManager()

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("title",)

    def __str__(self):
        return self.title
