import csv
import sqlite3
import sys

from django.core.management.base import BaseCommand
from django.db import DatabaseError

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
        # 'genre_title': Title,
    }

    table_db = {'titles': 'title', 'genre': 'genre', 'category': 'category', 'users': 'user', 'review': 'review', 'comments': 'comment'}

    def get_fields_db(self, file_name):
        """Получаем список имён колонок таблицы в базе данных"""
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.execute(
            f'select * from reviews_{self.table_db[file_name]}'
        )
        return [description[0] for description in cursor.description]

    def fields_verification(self, fields_csv, fields_db):
        if fields_csv == fields_db:
            return fields_csv
        return None

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
                with open(
                    f'static/data/{file_name}.csv', encoding='UTF-8'
                ) as file_csv:
                    reader = csv.DictReader(file_csv)
                    for row in reader:
                        print(row)
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
