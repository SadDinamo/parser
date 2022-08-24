import requests, time
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
from .models import News, NewsKeyWord, Share, Preference
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import json

# ***** Yahoo news Parser section *****

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'accept': '*/*',
}


def getHtml(shareName='SAVA', params=None):
    url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=' + shareName + '&region=US&lang=en-US'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    # print('Parsing url: ' + url)
    html = s.get(url, headers=HEADERS, timeout=5, params=params)
    # print('Server respond code: ' + str(html.status_code))
    return html


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


current_ticker_counter = 0
total_tickers = 0
ticker_name = ''
yahoo_ticker_update = False


def get_yahoo_ajax_progress_bar(request):
    global current_ticker_counter, total_tickers, ticker_name, yahoo_ticker_update
    result = {'total_tickers': total_tickers,
              'current_ticker_counter': current_ticker_counter,
              'ticker_name': ticker_name,
              'yahoo_ticker_update': yahoo_ticker_update
              }
    return JsonResponse(result)


def parse(request):
    global current_ticker_counter, total_tickers, ticker_name, yahoo_ticker_update
    yahoo_ticker_update = True
    tickers = Share.objects.all()
    total_tickers = Share.objects.count()
    current_ticker_counter = 0
    html_template = Preference.objects.filter(name='YahooNewsHtmlMessageTemplate').first()
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
                        current_html = current_html.replace('\'+new_news_item.pubDate+\'', news_item.find('pubDate').get_text())
                        current_html = current_html.replace('\'+new_news_item.description+\'', new_news_item.description)
                        current_html = current_html.replace('\'+new_news_item.link+\'', new_news_item.link)
                        send_mail('[Shares news parser] ' + new_news_item.title,
                                  new_news_item.link + '\n\n' + new_news_item.description,
                                  settings.EMAIL_HOST_USER,
                                  settings.RECIPIENT_LIST,
                                  html_message=current_html,
                                  )
            current_ticker_counter += 1
            ticker_name = getTickerCode(ticker)
        else:
            print('Error on server side: ' + xml.status_code)
    yahoo_ticker_update = False
    messages.add_message(request, messages.SUCCESS, 'Yahoo.Finance news info update finished')
