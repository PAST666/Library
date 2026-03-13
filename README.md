
# API сервис библиотеки

> [Техническое задание](./TASKS.md)

---

## Описание проекта

# REST API для управления библиотекой. 
# API предоставляет возможности для управления книгами, авторами и пользователями, а также предоставляет возможность отслеживать выдачу книг пользователям. 



---

## Стек технологий

- Python
- Django 4
- Django REST Framework (DRF)
- PostgreSQL
- Simple JWT

## Как запустить проект

Шаги для локального запуска проекта:

1. Клонировать репозиторий и перейти в директорию проекта:

```bash
git clone https://github.com/PAST666/Library
```

2. Создать виртуальное окружение и активировать его:

    - **Windows (GitBash)**:

      ```bash
      python -m venv .venv
      source .venv\Scripts\activate
      ```

    - **MacOS/Linux**:

      ```bash
      python -m venv .venv
      source .venv/bin/activate
      ```

3. Установить зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Настроить переменные окружения:

- Создайте файл `.env` и добавьте параметры из `.env.sample`.

5. Применить миграции базы данных:

    ```bash
 
   poetry run python manage.py makemigrations authors
   poetry run python manage.py makemigrations books
   poetry run python manage.py makemigrations users
    ```

6. Создать суперпользователя:

    ```bash
    poetry run python manage.py createsuperuser
    ```

7. Запустить сервер:

    ```bash
    poetry run python manage.py runserver
    ```

Сервис будет доступен по адресу: http://127.0.0.1:8000/

---

## Эндпоинты API

### Документация API

- Redoc - http://127.0.0.1:8000/redoc/
- Swagger - http://127.0.0.1:8000/swagger/

### Управление VPS:

- `GET /api/vps/` - получить список всех серверов;
- `GET /api/vps/?status=started` - получить список серверов с фильтрацией по статусу;
- `GET /api/vps/{uid}/` - получить информацию о конкретном сервере;
- `POST /api/vps/` - создать новый сервер;
- `PUT /api/vps/{uid}/` - обновить характеристики сервера;
- `DELETE /api/vps/{uid}/` - удалить сервер.

---

## Запуск тестов

- Для запуска тестов выполнить команду

```bash
poetry run coverage manage.py test
```

- Проверьте статус тестового покрытия проекта:

```bash
poetry run coverage report
```

---

## Автор

**Александр Топычканов**
