from typing import Any

from django.db import models
from django.db.models import Count


class AuthorManager(models.Manager):
    def get_all_authors(self) -> models.QuerySet:
        return self.all()

    def search_authors(self, **kwargs) -> models.QuerySet:
        valid_filters: dict[str, str] = {
            "books_title": "books__title__icontains",
            "nationality": "nationality",
            "books_genre": "books__genre__name__icontains",
        }

        filters: dict[str, Any] = {}
        for field, value in kwargs.items():
            if valid_filters.get(field) is None:
                continue
            if value is not None:
                filters[valid_filters[field]] = value
        queryset = self.all()
        if filters:
            queryset = queryset.filter(**filters).distinct()
        return queryset

    def _annotate_by(self) -> models.QuerySet:
        return self.annotate(books_count=Count("books")).filter(
            books_count__gt=0
        )
