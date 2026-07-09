# Ревью 2

## Нужно исправить

1. Проваливаются тесты, ниже трейс ошибок:

```commandline
FAILED tests/books/test_models.py::TestGenreModel::test_isbn_is_not_unique - django.core.exceptions.ValidationError: {'isbn': ['Книга with this ISBN already exists.']}
FAILED tests/books/test_models.py::TestGenreModel::test_age_rating_is_valid - django.core.exceptions.ValidationError: {'isbn': ['Invalid ISBN: Failed checksum']}
FAILED tests/books/test_models.py::TestGenreModel::test_create_book_without_user - django.core.exceptions.ValidationError: {'user': ['This field cannot be blank.']}
FAILED tests/books/test_models.py::TestBookManagerModel::test_search_books - assert [] == [<Book: Война и мир>]
FAILED tests/users/test_models.py::TestUserModel::test_create_valid_user - AssertionError: assert False is True
```

2. Примени и добавь миграции перед пушем.
3. Проверь проект перед отправкой, проходят ли все тесты.
4. Не забудь применить линтеры кода.
5. Создай PR после исправления ошибок.

---

## Желательно исправить

> [!TIP]
> Метод `test_check_roles`, уже создал ишью, посмотри пожалуйста.
