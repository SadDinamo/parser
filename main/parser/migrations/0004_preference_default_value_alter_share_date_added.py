# Generated by Django 4.0.3 on 2022-06-14 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0003_alter_preference_name_alter_share_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='default_value',
            field=models.CharField(max_length=40, null=True, verbose_name='default_value'),
        ),
        migrations.AlterField(
            model_name='share',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 14, 13, 34, 12, 333862), verbose_name='date_added'),
        ),
    ]
