from django.db import models


class AuthorManager(models.Manager):
    def get_all_authors(self) -> models.QuerySet:
        return self.all()

    def by_genre(self, genre: str) -> models.QuerySet:
        return self.filter(genre=genre)
