from django.core.management.base import BaseCommand
import csv

from reviews.models import Category, Comment, Genre


class Command(BaseCommand):
    help = 'Залить данные из файлов csv в базу данных'
    data = {
        'category.csv': Category,
        # 'genre_title.csv': Genre,
        # 'comments.csv': Comment,
    }

    def handle(self, *args, **kwargs):
        for i in self.data:
            with open(f'static/data/{i}', encoding='UTF-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    print(row)
                    self.data[i].objects.create(**row)

        # time = timezone.now().strftime('%X')
        # self.stdout.write(f"Текущее время: {time}")
