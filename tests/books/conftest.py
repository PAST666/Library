import pytest

from authors.models import Author
from datetime import date

from books.models import Genre
from users.models import User


@pytest.fixture
def author():
    author = Author.objects.create(
        first_name="Александр",
        last_name="Пушкин",
        birth_date=date(1811, 1, 10)
    )
    return author


@pytest.fixture
def author2():
    author = Author.objects.create(
        first_name="Лев",
        last_name="Толстой",
        birth_date=date(1811, 1, 10)
    )
    return author


@pytest.fixture
def user():
    username = User.objects.create(
        first_name="Иван",
        last_name="Иванов",
        email="user@yandex.ru",
        birth_date=date(1990, 1, 1),
        role="USER",
        password="securepass123"
    )
    return username


@pytest.fixture
def genre():
    return Genre.objects.create(
        name="Классика"
    )
