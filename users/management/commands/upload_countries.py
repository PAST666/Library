import json
import os

from django.core.management.base import BaseCommand
from users.models import Country


class Command(BaseCommand):
    help = "Загрузить список стран из файла countries.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "filepath",
            nargs="?",
            default="data/countries.json",
            help="Путь до файла со странами"
        )

    def handle(self, *args, **kwargs):
        filepath = kwargs.get("filepath")

        try:
            self.upload_countries(filepath)
            self.stdout.write(self.style.SUCCESS("Список стран успешно загружен"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Файл '{filepath}' не найден"))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка декодирования JSON: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Произошла ошибка: {e}"))

    def upload_countries(self, filepath: str) -> None:
        actions = {
            ".json": self.upload_countries_from_json,
            # ".csv": self.upload_countries_from_csv,
        }
        _, ext = os.path.splitext(filepath)

        ext = ext.lower()
        if ext not in actions:
            raise ValueError(f"Неизвестный формат файла: {ext}")

        action = actions.get(ext)
        action(filepath)

    def upload_countries_from_json(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            countries_data = json.load(f)
        countries = [Country(name=country["name"], code=country["code"]) for country in countries_data]
        Country.objects.bulk_create(countries)
