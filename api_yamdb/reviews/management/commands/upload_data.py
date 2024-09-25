import csv
import sys

from django.core.management.base import BaseCommand
from django.db import DatabaseError
from reviews.constants import LOCATION_CSV
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Залить данные из файлов csv в базу данных'
    data = {
        'category': Category,
        'genre': Genre,
        'titles': Title,
        'users': User,
        'review': Review,
        'comments': Comment,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'write',
            type=str,
            help=(
                'Для выборочной загрузки файлов выполните команду: '
                'python manage.py upload_data write -F <имя_файла>'
            )
        )
        parser.add_argument('-F', '--file_name',)

    def handle(self, *args, **options):

        file_name = options['file_name']
        try:
            if file_name:
                self.data = {file_name: self.data[file_name]}
            for file_name, model in self.data.items():
                with open(
                    f'{LOCATION_CSV}{file_name}.csv', encoding='UTF-8'
                ) as file_csv:
                    reader = csv.DictReader(file_csv)
                    model.objects.bulk_create([model(**row) for row in reader])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Данные из файла {file_name}.csv внесены в базу'
                        )
                    )
        except OSError:
            self.stdout.write(
                self.style.ERROR('Could not open/read file:', file_name)
            )
            sys.exit()
        except DatabaseError as error:
            self.stdout.write(
                self.style.ERROR(
                    f'Ошибка базы данных: {error}, file_name:{file_name}')
            )
        except csv.Error as error:
            sys.exit(
                f'file {file_csv}, line {reader}: {reader.line_num} , {error}'
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {error}, file_name:{file_name}')
            )
