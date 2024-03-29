# Generated by Django 4.0.6 on 2023-01-26 11:23

import datetime
from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0006_alter_preference_default_value_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceVariables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='name')),
                ('value', models.CharField(max_length=80, null=True, verbose_name='value')),
            ],
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-pubDate'], 'verbose_name': 'новость', 'verbose_name_plural': 'новости'},
        ),
        migrations.AlterModelOptions(
            name='newskeyword',
            options={'ordering': [django.db.models.functions.text.Upper('keyword'), 'keyword'], 'verbose_name': 'ключевое слово', 'verbose_name_plural': 'ключевые слова'},
        ),
        migrations.AlterField(
            model_name='share',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 14, 23, 29, 67250), verbose_name='date_added'),
        ),
    ]
