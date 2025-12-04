import json
from django.core.management.base import BaseCommand
from users.models import Country


class Command(BaseCommand):
    help = 'Загрузить список стран из файла countries.json'

    def handle(self, *args, **kwargs):
        try:
            with open('data/countries.json', 'r', encoding='utf-8') as f:
                countries = json.load(f)

                for country in countries:
                    Country.objects.create(name=country['name'], code=country['code'])
            self.stdout.write(self.style.SUCCESS('Countries loaded successfully'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Ошибка декодирования JSON: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
