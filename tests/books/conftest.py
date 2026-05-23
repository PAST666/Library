import pytest

from authors.models import Author
from users.models import User


@pytest.fixture
def author():
    author = Author.objects.create(
        first_name="Александр",
        last_name="Пушкин",
        birth_date="10.01.1811"
    )
    return author

def author2():
    author = Author.objects.create(
        first_name="Лев",
        last_name="Толстой",
        birth_date="11.01.1812"
    )
    return author


def user():
    username = User.objects.create(
        first_name="Иван",
        last_name="Иванов",
        email="user@yandex.ru",
        role="USER"
    )
    return username
