# Generated by Django 3.2 on 2024-07-13 12:30

from django.db import migrations, models
import reviews.validates


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_auto_20240712_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(db_index=True, validators=[reviews.validates.validate_year], verbose_name='Год выпуска'),
        ),
    ]
