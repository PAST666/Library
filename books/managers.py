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
            "publication_year" : "publication_year",
            "pages": "pages"
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

    def available(self) -> models.QuerySet:
        return self.annotate(
            available_count=Count(
                "book_inventory",
                filter=Q(book_inventory__status=Status.AVAILABLE)
            )
        ).filter(available_count__gt=0)

    def busy(self) -> models.QuerySet:
        return self.annotate(
            busy_count=Count(
                "book_inventory",
                filter=Q(book_inventory__status=Status.BUSY)
            )
        ).filter(busy_count__gt=0)

    def reserved(self) -> models.QuerySet:
        return self.annotate(
            reserved_count=Count(
                "book_inventory",
                filter=Q(book_inventory__status=Status.RESERVED)
            )
        ).filter(reserved_count__gt=0)

    def by_genre(self, genre: str) -> models.QuerySet:
        return self.filter(genre=genre)

    def recent(self, years: int = 5) -> models.QuerySet:
        return self.filter(publication_date__gte=datetime.now().year - years)


