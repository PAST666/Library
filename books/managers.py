from django.db import models


class BookManager(models.Manager):
    def get_all_books_list(self) -> models.QuerySet:
        return self.all()

    def search_books(self, title=None, genre=None, publication_year=None, pages=None):
        queryset = self.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre=genre)
        if publication_year:
            queryset = queryset.filter(publication_year=publication_year)
        if pages:
            queryset = queryset.filter(pages=pages)
        return queryset
