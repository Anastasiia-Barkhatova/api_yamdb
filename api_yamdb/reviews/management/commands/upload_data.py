import csv
import sys

from django.core.management.base import BaseCommand
from django.db import DatabaseError

from reviews.models import Category, Comment, Genre, Review, Title


class Command(BaseCommand):
    help = 'Залить данные из файлов csv в базу данных'
    data = {
        'category.csv': Category,
        'comments.csv': Comment,
        'genre_title.csv': Title,
        'genre.csv': Genre,
        'review.csv': Review,
        'titles.csv': Title,
        'users.csv': Genre,
    }

    def handle(self, *args, **kwargs):
        try:
            for file_name, model in self.data.items():
                try:
                    file_csv = open(
                        f'static/data/{file_name}', encoding='UTF-8'
                    )
                except OSError:
                    print('Could not open/read file:', file_name)
                    sys.exit()
                with file_csv:
                    reader = csv.DictReader(file_csv)
                    for row in reader:
                        print(row)
                        model.objects.create(**row)
                        file_csv.close()

        except DatabaseError as error:
            print(error)
