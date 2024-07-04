import csv
import sys

from django.core.management.base import BaseCommand
from django.db import DatabaseError

from reviews.models import Category, Comment, Genre, Review, Title


class Command(BaseCommand):
    help = 'Залить данные из файлов csv в базу данных'
    data = {
        'category': Category,
        'comments': Comment,
        'genre_title': Genre_Title,
        'genre': Genre,
        'review': Review,
        'titles': Title,
        'users': Genre,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help=(
                'Укажите имя файла который необходимо загрузить в базу.'
                'Для загрузки всех файлов из директории, укажите - "all"'
            )
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        try:
            if file_name != 'all':
                self.data = {file_name: self.data[file_name]}
            for file_name, model in self.data.items():
                try:
                    file_csv = open(
                        f'static/data/{file_name}.csv', encoding='UTF-8'
                    )
                except OSError:
                    self.stdout.write(
                        self.style.ERROR(
                            'Could not open/read file:', file_name
                        )
                    )
                    sys.exit()
                with file_csv:
                    reader = csv.DictReader(file_csv)
                    for row in reader:
                        model.objects.create(**row)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Данные из файла {file_name}.csv внесены в базу'
                        )
                    )
        except DatabaseError as error:
            self.stdout.write(self.style.ERROR(f'Ошибка базы данных {error}'))
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
