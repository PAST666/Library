# Ревью 1

## Нужно исправить

> [!WARNING]
> В директории `tests` и во всех её поддиректориях отсутствуют файлы `__init__.py`

### `TestNationalityModel`

| Кейс       | Примечание |
|------------|------------|
| TC-NAT-003 | Пропущен   |

### `TestAuthorModel`

| Кейс       | Примечание |
|------------|------------|
| TC-AUT-012 | Пропущен   |

- `test_max_len_first_name_150_symbols` - не вызывает `refresh_from_db()` и проверяет in-memory объект, не БД.
  Добавь `author.refresh_from_db()` перед `assert` как в тесте `test_max_len_nationality_field_150_symbols`

- `BookManagerModel` - классы без префикса `Test`, `pytest` по умолчанию собирает только классы начинающиеся с `Test`,
  значит ни один тест из этого класса не был проверен.
- Также три метода написаны без префикса `test_` из-за этого `pytest` их не видит:
    - `isbn_is_not_unique`
    - `age_rating_is_valid`
    - `create_some_examples_of_book`
- `test_without_publication_date` - написан некорректно, но проходит проверку. Он падает не из-за отсутствия даты,
  а в `pages` передается значение `-1`.
- `test_create_book_without_user` - в этом тесте ты ожидаешь `ValidationError`, но `user` опциональный, и запись должна
  создаться успешно. Посмотри ещё раз условие кейса `TC-BOK-014`.

```python
class Book(models.Model):
    # ...
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пользователь",
        related_name="books",
        db_index=True
    )
    # ...
```

- `test_usermanager_createsuperuser` - не нужно передавать `role="ADMIN"` в метод `create_superuser`, а метод сам должен
  создать пользователя с ролем админа. В этом и суть проверки. А в `assert` где проверяешь роль, перепиши проверку через
  enum-класс `Roles.ADMIN`.
- `test_name_field_max_valid_len_20_symbols` - не дописан тест.
- `test_check_roles` - надо убрать все проверки через строку, используй методы, которые уже есть в модели: `is_admin`
  `is_moderator` и т.д.

---

## Замечания по качеству кода:

- Написал фикстуры - это отлично, но они не применяются в тестах (только фикстура `user` используешь в тестах-books).
- Нужно использовать фикстуры, чтобы не создавать объекты вручную с повторяющимся данными.

например:

```python
expected_date = date(1990, 1, 1)
author = Author(first_name="Иван", last_name="Иванов", birth_date=expected_date)
```

повторяется в каждом тесте, можно вынести в фикстуру или хотя бы в `setup_method`:

```python
@pytest.fixture
def author_data():
    return {"first_name": "Иван", "last_name": "Иванов", "birth_date": date(1990, 1, 1)}
```

и в тестах использовать можно так:

```python
def test_something(self, valid_author_data):
    author = Author(**valid_author_data)
```

> [!NOTE]
> В целом все выполнено хорошо, для первого теста это отличная работа. Желательно исправить замечания по коду. Или
> можешь это учитывать и в будущих проектах применить подходы с фикстурами.
