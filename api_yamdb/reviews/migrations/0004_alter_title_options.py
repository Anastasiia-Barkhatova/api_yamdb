# Generated by Django 3.2 on 2024-07-10 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-name',), 'verbose_name': 'произведение', 'verbose_name_plural': 'произведения'},
        ),
    ]
