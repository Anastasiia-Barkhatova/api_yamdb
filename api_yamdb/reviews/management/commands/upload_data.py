import csv
import sys
import sqlite3

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

    def column_validation(self, file_name, model):

        pass

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help=(
                'Укажите имя файла который необходимо загрузить в базу.'
                'Для загрузки всех файлов из директории, укажите - "all"'
            ),
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
                    print(file_csv.readline())
                    file_csv.seek(0)

                    connection = sqlite3.connect('db.sqlite3')
                    cursor = connection.execute(f'select * from reviews_{file_name}')
                    names = [description[0] for description in cursor.description]
                    print(names)

                    #conn = sqlite3.connect('db.sqlite3')
                    #c = conn.cursor()
                    #c.execute(f'select * from reviews_{file_name}')
                    #print([member[0] for member in c.description])

                except OSError:
                    self.stdout.write(
                        self.style.ERROR(
                            'Could not open/read file:', file_name
                        )
                    )
                    sys.exit()
                with file_csv:
                    reader = csv.DictReader(file_csv)
                    model.objects.bulk_create([model(**row) for row in reader])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Данные из файла {file_name}.csv внесены в базу'
                        )
                    )
        except DatabaseError as error:
            self.stdout.write(self.style.ERROR(f'Ошибка базы данных: {error}'))
        except csv.Error as error:
            sys.exit(
                f'file {file_csv}, line {reader}: {reader.line_num} , {error}'
            )
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
