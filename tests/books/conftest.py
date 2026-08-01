from datetime import date

import pytest

from authors.models import Author
from books.constants import Status
from books.models import Book, Genre
from users.models import User


@pytest.fixture
def author():
    author = Author.objects.create(
        first_name="Александр",
        last_name="Пушкин",
        birth_date=date(1811, 1, 10),
    )
    return author


@pytest.fixture
def author2():
    author = Author.objects.create(
        first_name="Лев", last_name="Толстой", birth_date=date(1811, 1, 10)
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
        password="securepass123",
    )
    return username


@pytest.fixture
def genre():
    return Genre.objects.create(name="Классика")


@pytest.fixture
def genre_data():
    return {
        "name": "Фантастика",
    }


@pytest.fixture
def genre_data_2():
    return {
        "name": "Детектив",
    }


@pytest.fixture
def book_inventory_data(book):
    return {
        "book": book,
        "status": Status.AVAILABLE,
    }


@pytest.fixture
def book(book_data):
    return Book.objects.create(**book_data)


@pytest.fixture
def book_data(user):
    return {
        "title": "Фантастика",
        "pages": 300,
        "publication_date": date(2016, 1, 1),
        "isbn": "9780306406157",
        "age_rating": "ABOVE_ZERO",
        "user": user,
    }


@pytest.fixture
def book_data_2(user):
    return {
        "title": "Фантастика",
        "pages": 300,
        "publication_date": date(2023, 1, 1),
        "isbn": "9785171124403",
        "age_rating": "ABOVE_SIX",
        "user": user,
    }


@pytest.fixture
def book_data_3(user):
    return {
        "title": "Фантастика",
        "pages": 300,
        "publication_date": date(2026, 1, 1),
        "isbn": "9785699120147",
        "age_rating": "ABOVE_TWELVE",
        "user": user,
    }


@pytest.fixture
def book_data_4(user):
    return {
        "title": "Фантастика",
        "pages": 300,
        "publication_date": date(2020, 1, 1),
        "isbn": "9785389062566",
        "age_rating": "ABOVE_SIXTEEN",
        "user": user,
    }


@pytest.fixture
def book_data_5(user):
    return {
        "title": "Фантастика",
        "pages": 300,
        "publication_date": date(2020, 1, 1),
        "isbn": "9785170906222",
        "age_rating": "ABOVE_EIGHTEEN",
        "user": user,
    }
