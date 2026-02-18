from django.db import models
from typing import Any


class AuthorManager(models.Manager):
    def get_all_authors(self) -> models.QuerySet:
        return self.all()

    def search_authors(self, **kwargs) -> models.QuerySet:
        valid_filters: dict[str, str] = {
            "title": "title__icontains",
            "genre": "genre",
            "nationality": "nationality",
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
