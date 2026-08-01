from datetime import datetime
from typing import Any

from django.db import models
from django.db.models import Count, Q

from .constants import Status


class BookManager(models.Manager):
    def get_all_books_list(self) -> models.QuerySet:
        return self.all()

    def search_books(self, **kwargs) -> models.QuerySet:
        valid_filters: dict[str, str] = {
            "title": "title__icontains",
            "genre": "genre",
            "publication_date": "publication_date__year",
            "pages": "pages",
        }

        filters: dict[str, Any] = {}
        for field, value in kwargs.items():
            if valid_filters.get(field) is None:
                continue
            if value is not None:
                filters[valid_filters[field]] = value
        queryset = self.all()
        if filters:
            queryset = queryset.filter(**filters)

        return queryset

    def _annotate_by(self, status) -> models.QuerySet:
        return self.annotate(
            status_count=Count(
                "book_inventory", filter=Q(book_inventory__status=status)
            )
        ).filter(status_count__gt=0)

    def available(self):
        return self._annotate_by(Status.AVAILABLE)

    def busy(self):
        return self._annotate_by(Status.BUSY)

    def reserved(self):
        return self._annotate_by(Status.RESERVED)

    def by_genre(self, genre: str) -> models.QuerySet:
        return self.filter(genre=genre)

    def recent(self, years: int = 5) -> models.QuerySet:
        return self.filter(
            publication_date__year__gte=datetime.now().year - years
        )
