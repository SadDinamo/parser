import requests, time
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
from .models import News, NewsKeyWord, Share, Preference, ServiceVariables
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import json


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'accept': '*/*',
}

HEADERS_CNN = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.0.2500 Yowser/2.5 Safari/537.36',
    'accept': '*/*',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors'
}


def getHtml(shareName='SAVA', params=None):
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=' + shareName + '&region=US&lang=en-US'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS, timeout=5, params=params)
    return html


def getHtmlNasdaqFailsToDeliverList(params=None):
    tickers = Share.objects.all()
    table = []
    row = []
    url = 'https://nasdaqtrader.com/trader.aspx?id=RegSHOThreshold'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS, timeout=5, params=params)
    if html.status_code == 200:  # success
        bs_content = BeautifulSoup(html.text, 'html.parser')
        div = bs_content.find(id='threshold')
        items = div.find_all('tr')
        for item in items:
            tags_td = item.find_all('td')
            if len(tags_td) > 0:
                for tag in tags_td:
                    row.append(str(tag))
                    check = False
                    for ticker in tickers:
                        if str(row[0]) == '<td>' + ticker.ticker + '</td>':
                            check = True
                if check:
                    row.append('tradable')
                else:
                    row.append('non-tradable')
                table.append(row)
                row = []
    return table


def getHtmlFinvizTopShorts(params=None):
    tickers = Share.objects.all()
    shorts = []
    url = 'https://finviz.com/screener.ashx?v=111&f=cap_microover&o=-shortinterestshare'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS, timeout=5, params=params)
    if html.status_code == 200:  # success
        bs_content = BeautifulSoup(html.text, 'html.parser')
        div = bs_content.find(id='screener-views-table')
        sub_div = div.findAll('a', attrs={'class': 'screener-link-primary'})
        for item in sub_div:
            if tickers.filter(ticker=item.text):
                shorts.append(item.text)
    return shorts


def getFinvizCrypto(params=None):
    url = 'https://finviz.com/api/crypto_all.ashx?timeframe=m5'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS_CNN, timeout=5)
    if html.status_code == 200:  # success
        bs_content = BeautifulSoup(html.text, 'html.parser')
        result = json.loads(bs_content.text)
        print(result)
    else:
        result = html.content
    return JsonResponse(result)


def getCnnFearAndGreedStats(request):
    url = 'https://production.dataviz.cnn.io/index/fearandgreed/graphdata/'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS_CNN, timeout=15)
    if html.status_code == 200:  # success
        bs_content = BeautifulSoup(html.text, 'html.parser')
        result = json.loads(bs_content.text)
    else:
        result = html.content
    return JsonResponse(result)


def getFinvizFuturesData(request):
    url = 'https://finviz.com/api/futures_all.ashx?timeframe=d1'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS_CNN, timeout=5)
    if html.status_code == 200:  # success
        bs_content = BeautifulSoup(html.text, 'html.parser')
        result = json.loads(bs_content.text)
    else:
        result = html.content
    return JsonResponse(result)


def getTickerCode(ticker: Share):
    if ticker.class_code == 'SPBXM':
        ticker_corrected = ticker.ticker
    elif ticker.class_code == 'SPBDE':
        ticker_corrected = ticker.ticker[:ticker.ticker.find('@')] + '.DE'
    elif ticker.class_code == 'TQBR' or ticker.class_code == 'SPBRU_USD':
        ticker_corrected = ticker.ticker + '.ME'
    elif ticker.class_code == 'SPBHKEX':
        if len(ticker.ticker) < 4:
            ticker_corrected = ticker.ticker.zfill(4) + '.HK'
        else:
            ticker_corrected = ticker.ticker + '.HK'
    else:
        ticker_corrected = ticker.ticker
    return ticker_corrected


def get_yahoo_ajax_progress_bar(request):
    global current_ticker_counter, total_tickers, ticker_name, yahoo_ticker_update
    result = {'total_tickers': ServiceVariables.objects.filter(name='total_tickers').first().value,
              'current_ticker_counter': ServiceVariables.objects.filter(name='current_ticker_counter').first().value,
              'ticker_name': ServiceVariables.objects.filter(name='ticker_name').first().value,
              'yahoo_ticker_update': ServiceVariables.objects.filter(name='yahoo_ticker_update').first().value == 'True'
              }
    return JsonResponse(result)


def parse(request):
    # global current_ticker_counter, total_tickers, ticker_name, yahoo_ticker_update
    yahoo_ticker_update = ServiceVariables.objects.filter(name='yahoo_ticker_update').first()
    yahoo_ticker_update.value = 'True'
    yahoo_ticker_update.save()

    total_tickers = ServiceVariables.objects.filter(name='total_tickers').first()
    total_tickers.value = str(Share.objects.count())
    total_tickers.save()

    current_ticker_counter = ServiceVariables.objects.filter(name='current_ticker_counter').first()
    current_ticker_counter.value = '0'
    current_ticker_counter.save()

    html_template = Preference.objects.filter(name='YahooNewsHtmlMessageTemplate').first()
    tickers = Share.objects.all()
    for ticker in tickers:
        xml = getHtml(getTickerCode(ticker))
        if xml.status_code == 200:  # success
            bs_content = BeautifulSoup(xml.text, 'xml')
            items = bs_content.find_all('item')
            news_key_words = NewsKeyWord.objects.all()
            for news_item in items:
                for news_key_word in news_key_words:
                    if news_item.find('title').get_text().find(news_key_word.keyword) > 0 \
                            and not News.objects.filter(title=news_item.find('title').get_text()):
                        new_news_item = News(
                            description=news_item.find('description').get_text(),
                            link=news_item.find('link').get_text(),
                            pubDate=datetime.strptime(news_item.find('pubDate').get_text(), '%a, %d %b %Y %H:%M:%S %z'),
                            title=news_item.find('title').get_text(),
                        )
                        new_news_item.save()
                        current_html = html_template.value.replace('\'+new_news_item.title+\'', new_news_item.title)
                        current_html = current_html.replace('\'+new_news_item.pubDate+\'',
                                                            news_item.find('pubDate').get_text())
                        current_html = current_html.replace('\'+new_news_item.description+\'',
                                                            new_news_item.description)
                        current_html = current_html.replace('\'+new_news_item.link+\'', new_news_item.link)
                        send_mail('[Shares news parser] ' + new_news_item.title,
                                  new_news_item.link + '\n\n' + new_news_item.description,
                                  settings.EMAIL_HOST_USER,
                                  settings.RECIPIENT_LIST,
                                  html_message=current_html,
                                  )

            current_ticker_counter.value = str(int(current_ticker_counter) + 1)
            current_ticker_counter.save()

            ticker_name = ServiceVariables.objects.filter(name='ticker_name').first()
            ticker_name.value = getTickerCode(ticker)
            ticker_name.save()
        else:
            print('Error on server side: ' + xml.status_code)
    yahoo_ticker_update.value = 'False'
    yahoo_ticker_update.save()
    messages.add_message(request, messages.SUCCESS, 'Yahoo.Finance news info update finished')


def parse_jahoo_finance_news_background(request):
    yahoo_ticker_update = ServiceVariables.objects.filter(name='yahoo_ticker_update').first()
    yahoo_ticker_update.value = 'True'
    yahoo_ticker_update.save()
    total_tickers = ServiceVariables.objects.filter(name='total_tickers').first()
    total_tickers.value = str(Share.objects.count())
    total_tickers.save()

    current_ticker_counter = ServiceVariables.objects.filter(name='current_ticker_counter').first()
    current_ticker_counter.value = '0'
    current_ticker_counter.save()

    tickers = Share.objects.all()
    for ticker in tickers:
        xml = getHtml(getTickerCode(ticker))
        if xml.status_code == 200:  # success
            bs_content = BeautifulSoup(xml.text, 'xml')
            items = bs_content.find_all('item')
            news_key_words = NewsKeyWord.objects.all()
            for news_item in items:
                for news_key_word in news_key_words:
                    if news_item.find('title').get_text().find(news_key_word.keyword) > 0 \
                            and not News.objects.filter(title=news_item.find('title').get_text()):
                        new_news_item = News(
                            description=news_item.find('description').get_text(),
                            link=news_item.find('link').get_text(),
                            pubDate=datetime.strptime(news_item.find('pubDate').get_text(), '%a, %d %b %Y %H:%M:%S %z'),
                            title=news_item.find('title').get_text(),
                        )
                        new_news_item.save()

            current_ticker_counter.value = str(int(current_ticker_counter.value) + 1)
            current_ticker_counter.save()

            ticker_name = ServiceVariables.objects.filter(name='ticker_name').first()
            ticker_name.value = getTickerCode(ticker)
            ticker_name.save()

        else:
            print('Error on server side: ' + xml.status_code)
    yahoo_ticker_update.value = 'False'
    yahoo_ticker_update.save()

