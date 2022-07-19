# Generated by Django 4.0.6 on 2022-07-19 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0004_preference_default_value_alter_share_date_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newskeyword',
            options={'verbose_name': 'ключевое слово', 'verbose_name_plural': 'ключевые слова'},
        ),
        migrations.AlterModelOptions(
            name='preference',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='preference',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='share',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 9, 15, 38, 601959), verbose_name='date_added'),
        ),
    ]
