from django.db import models

from .constants import MAX_NAME_LENGTH


class Author(models.Model):
    name: str = models.CharField(
        "Автор",
        max_length=MAX_NAME_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Автор"
    )
    birth_date = models.DateField(
        "Дата рождения"
    )
    nationality: str = models.CharField(
        "Национальность",
        max_length=MAX_NAME_LENGTH,
        null=True,
        blank=True,
        verbose_name="Национальность"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def __str__(self):
        return self.name
