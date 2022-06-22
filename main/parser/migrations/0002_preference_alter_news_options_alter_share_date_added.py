# Generated by Django 4.0.3 on 2022-06-13 05:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('value', models.CharField(max_length=40, verbose_name='value')),
            ],
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'новость', 'verbose_name_plural': 'новости'},
        ),
        migrations.AlterField(
            model_name='share',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 8, 46, 18, 566097), verbose_name='date_added'),
        ),
    ]