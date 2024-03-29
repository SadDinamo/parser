# Generated by Django 4.0.3 on 2022-05-17 07:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='description')),
                ('link', models.TextField(verbose_name='link')),
                ('pubDate', models.DateTimeField(verbose_name='pubDate')),
                ('title', models.TextField(verbose_name='title')),
            ],
        ),
        migrations.CreateModel(
            name='NewsKeyWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=30, verbose_name='keyword')),
            ],
            options={
                'verbose_name': 'ключевое слово',
                'verbose_name_plural': 'ключевые слова',
                'ordering': ['keyword'],
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('figi', models.CharField(max_length=12, verbose_name='figi')),
                ('ticker', models.CharField(max_length=20, verbose_name='ticker')),
                ('class_code', models.CharField(max_length=20, verbose_name='class_code')),
                ('isin', models.CharField(max_length=12, verbose_name='isin')),
                ('lot', models.IntegerField(null=True, verbose_name='lot')),
                ('currency', models.CharField(max_length=5, verbose_name='currency')),
                ('short_enabled_flag', models.BooleanField(null=True, verbose_name='shorts enabled')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('exchange', models.CharField(max_length=80, verbose_name='exchange')),
                ('ipo_date', models.DateTimeField(null=True, verbose_name='ipo_date')),
                ('issue_size', models.BigIntegerField(null=True, verbose_name='issue_size')),
                ('country_of_risk', models.CharField(max_length=2, verbose_name='country_of_risk')),
                ('country_of_risk_name', models.CharField(max_length=80, verbose_name='country_of_risk_name')),
                ('sector', models.CharField(max_length=25, verbose_name='sector')),
                ('issue_size_plan', models.BigIntegerField(null=True, verbose_name='issue_size_plan')),
                ('otc_flag', models.BooleanField(default=False, null=True, verbose_name='otc_flag')),
                ('buy_available_flag', models.BooleanField(default=False, null=True, verbose_name='buy_available_flag')),
                ('sell_available_flag', models.BooleanField(default=False, null=True, verbose_name='sell_available_flag')),
                ('div_yield_flag', models.BooleanField(default=False, null=True, verbose_name='div_yield_flag')),
                ('api_trade_available_flag', models.BooleanField(default=False, null=True, verbose_name='api_trade_available_flag')),
                ('date_added', models.DateTimeField(default=datetime.datetime(2022, 5, 17, 10, 41, 17, 605686), verbose_name='date_added')),
            ],
            options={
                'verbose_name': 'акция',
                'verbose_name_plural': 'акции',
                'ordering': ['ticker'],
            },
        ),
    ]
