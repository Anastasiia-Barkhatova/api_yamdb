# Generated by Django 3.2 on 2024-07-11 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_alter_title_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='genres',
            new_name='genre',
        ),
    ]
