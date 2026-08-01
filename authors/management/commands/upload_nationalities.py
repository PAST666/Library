import json
import os

from django.core.management.base import BaseCommand

from authors.models import Nationality


class Command(BaseCommand):
    help = "Загрузить список национальностей из файла nationalities.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "filepath",
            nargs="?",
            default="data/nationalities.json",
            help="Путь до файла с национальностями",
        )

    def handle(self, *args, **kwargs):
        filepath = kwargs.get("filepath")

        try:
            self.upload_nationalities(filepath)
            self.stdout.write(
                self.style.SUCCESS("Список национальностей успешно загружен")
            )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Файл '{filepath}' не найден"))
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка декодирования JSON: {e}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Произошла ошибка: {e}"))

    def upload_nationalities(self, filepath: str) -> None:
        actions = {
            ".json": self.upload_nationalities_from_json,
        }
        _, ext = os.path.splitext(filepath)

        ext = ext.lower()
        if ext not in actions:
            raise ValueError(f"Неизвестный формат файла: {ext}")

        action = actions.get(ext)
        action(filepath)

    def upload_nationalities_from_json(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        nationalities = [
            Nationality(nationality=n["nationality"], code=n["code"])
            for n in data
        ]
        created = Nationality.objects.bulk_create(
            nationalities, ignore_conflicts=True
        )
        if len(created):
            print(f"Добавлено {len(created)} национальностей")
        else:
            print("Новых национальностей не добавлено")
