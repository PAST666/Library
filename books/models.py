from authors.models import Author

from django.db import models
from django.core.validators import MinValueValidator
from isbn_field import ISBNField
from users.models import User

from .constants import (
    MAX_NAME_LENGTH,
    MAX_NUMBER_ISBN,
    MAX_AGE_RATING_LENGTH,
    MAX_STATUS_LENGTH,
    AgeRating,
    Status
)

from .managers import BookManager


class Genre(models.Model):
    name: str = models.CharField(
        "Жанр",
        max_length=MAX_NAME_LENGTH,
        db_index=True,
        unique=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title: str = models.CharField(
        "Книга",
        max_length=MAX_NAME_LENGTH,
        db_index=True
    )
    pages: int = models.PositiveSmallIntegerField(
        "Количество страниц",
        validators=[MinValueValidator(1)]
    )
    publication_date = models.DateField(
        "Дата издания"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пользователь",
        related_name="books",
        db_index=True
    )
    author = models.ManyToManyField(
        "Author",
        verbose_name="Автор",
        related_name="books"
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        related_name="books"
    )
    isbn: str = ISBNField(
        "ISBN",
        max_length=MAX_NUMBER_ISBN,
        unique=True
    )
    age_rating: str = models.CharField(
        "Возрастной рейтинг",
        choices=AgeRating.choices,
        max_length=MAX_AGE_RATING_LENGTH
    )
    objects = BookManager()

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("title",)

    @property
    def is_for_child(self) -> bool:
        return self.age_rating in ["ABOVE_ZERO", "ABOVE_SIX"]

    @property
    def is_for_teenager(self) -> bool:
        return self.age_rating in ["ABOVE_TWELVE", "ABOVE_SIXTEEN"]

    @property
    def is_for_adult(self) -> bool:
        return self.age_rating == "ABOVE_EIGHTEEN"

    def __str__(self):
        return self.title


class BookInventory(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Книга",
        related_name="book_inventory",
        db_index=True
    )
    status: str = models.CharField(
        "Статус",
        choices=Status.choices,
        max_length=MAX_STATUS_LENGTH
    )

    class Meta:
        verbose_name = "Перечень книг"
        verbose_name_plural = "Перечни книг"
        ordering = ("status",)

    def __str__(self):
        return f"{self.book.title[:15]} | {self.book.isbn} -> {self.status}"
