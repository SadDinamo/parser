from builtins import str
from tinkoff.invest import Client
from django.db import models
from django.urls import reverse
from django.core import serializers
from datetime import datetime
from tinkoff.invest import Client


class Share(models.Model):
    figi = models.CharField(verbose_name='figi', max_length=12)
    ticker = models.CharField(verbose_name='ticker', max_length=20)
    class_code = models.CharField(verbose_name='class_code', max_length=20)
    isin = models.CharField(verbose_name='isin', max_length=12)
    lot = models.IntegerField(verbose_name='lot', null=True)
    currency = models.CharField(verbose_name='currency', max_length=5)
    short_enabled_flag = models.BooleanField(verbose_name='shorts enabled', null=True)
    name = models.CharField(verbose_name='name', max_length=80)
    exchange = models.CharField(verbose_name='exchange', max_length=80)
    ipo_date = models.DateTimeField(verbose_name='ipo_date', null=True)
    issue_size = models.BigIntegerField(verbose_name='issue_size', null=True)
    country_of_risk = models.CharField(verbose_name='country_of_risk', max_length=2)
    country_of_risk_name = models.CharField(verbose_name='country_of_risk_name', max_length=80)
    sector = models.CharField(verbose_name='sector', max_length=25)
    issue_size_plan = models.BigIntegerField(verbose_name='issue_size_plan', null=True)
    otc_flag = models.BooleanField(verbose_name='otc_flag', default=False, null=True)
    buy_available_flag = models.BooleanField(verbose_name='buy_available_flag', default=False, null=True)
    sell_available_flag = models.BooleanField(verbose_name='sell_available_flag', default=False, null=True)
    div_yield_flag = models.BooleanField(verbose_name='div_yield_flag', default=False, null=True)
    api_trade_available_flag = models.BooleanField(verbose_name='api_trade_available_flag', default=False, null=True)
    date_added = models.DateTimeField(verbose_name='date_added', default=datetime.now())

    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'акции'
        ordering = ['ticker']


class NewsKeyWord(models.Model):
    keyword = models.CharField(verbose_name='keyword', max_length=30)

    class Meta:
        verbose_name = 'ключевое слово'
        verbose_name_plural = 'ключевые слова'

    def get_absolute_url(self):
        return reverse('news_key_words_list')

    def get_update_url(self):
        return reverse('news_key_words_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('news_key_words_delete', kwargs={'pk': self.pk})


class News(models.Model):
    description = models.TextField(verbose_name='description')
    link = models.TextField(verbose_name='link')
    pubDate = models.DateTimeField(verbose_name='pubDate')
    title = models.TextField(verbose_name='title')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Preference(models.Model):
    name = models.CharField(verbose_name='name', max_length=40, unique=True)
    value = models.TextField(verbose_name='value')
    default_value = models.TextField(verbose_name='default_value', null=True)
    description = models.TextField(verbose_name='description', null=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('preferences')

    def get_update_url(self):
        return reverse('preference_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('preference_delete', kwargs={'pk': self.pk})

