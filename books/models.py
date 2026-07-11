from django.core.validators import MinValueValidator
from django.db import models
from isbn_field import ISBNField

from .constants import (
    MAX_AGE_RATING_LENGTH,
    MAX_NAME_LENGTH,
    MAX_NUMBER_ISBN,
    MAX_STATUS_LENGTH,
    AgeRating,
    Status,
)
from .managers import BookManager
from users.models import User


class Genre(models.Model):
    name: str = models.CharField(
        "Жанр", max_length=MAX_NAME_LENGTH, db_index=True, unique=True
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
        "Книга", max_length=MAX_NAME_LENGTH, db_index=True
    )
    pages: int = models.PositiveSmallIntegerField(
        "Количество страниц", validators=[MinValueValidator(1)]
    )
    publication_date = models.DateField("Дата издания")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        related_name="books",
    )
    author = models.ManyToManyField(
        "authors.Author", verbose_name="Автор", related_name="books"
    )
    genre = models.ManyToManyField(
        Genre, verbose_name="Жанр", related_name="books"
    )
    isbn: str = ISBNField("ISBN", max_length=MAX_NUMBER_ISBN, unique=True)
    age_rating: str = models.CharField(
        "Возрастной рейтинг",
        choices=AgeRating.choices,
        max_length=MAX_AGE_RATING_LENGTH,
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
        on_delete=models.CASCADE,
        verbose_name="Книга",
        related_name="book_inventory",
    )
    status: str = models.CharField(
        "Статус", choices=Status.choices, max_length=MAX_STATUS_LENGTH
    )
    curr_holder = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="borrowed_items",
    )
    borrowed_at = models.DateTimeField("Дата выдачи", null=True, blank=True)
    due_date = models.DateField("Дата возврата", null=True, blank=True)

    class Meta:
        verbose_name = "Перечень книг"
        verbose_name_plural = "Перечни книг"
        ordering = ("status",)

    def __str__(self):
        return f"{self.book.title[:15]} | {self.book.isbn} -> {self.status}"
