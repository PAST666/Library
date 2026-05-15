import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from books.models import Genre


@pytest.mark.django_db
class TestGenreModel:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.object = Genre(
            name="Фантастика"
        )
        self.object.name = self.object.name.lower()
        self.object.full_clean()
        self.object.save()

    def test_genre_created(self):
        genre_from_db = Genre.objects.get(name="фантастика")
        assert genre_from_db.name == "фантастика"

    def test_empty_genre(self):
        empty_genre = Genre(name="")
        with pytest.raises(ValidationError):
            empty_genre.full_clean()

    def unique_field(self):
        self.genre = Genre(name="Фантастика")
        with pytest.raises(IntegrityError):
            self.genre.save()

    def len_150_symbols(self):
        self.genre = Genre(name="а"*150)
        self.genre.full_clean()
        self.genre.save()
        assert len(self.genre.name) == 150

    def len_151_symbols(self):
        self.genre = Genre(name="а" * 151)
        self.genre.full_clean()
        with pytest.raises(ValidationError):
            self.genre.save()

    def check_lower(self):
        self.genre = Genre(name="ФАНТАСТИКА")
        self.genre.full_clean()
        self.genre.save()
        assert self.genre.name == "фантастика"
