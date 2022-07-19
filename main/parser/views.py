import os

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import edit
from tinkoff.invest import Client
from django.views import generic
from .models import *
from django.contrib import messages
import datetime
from .parsers import parse, get_yahoo_ajax_progress_bar
from .forms import PreferenceForm, NewsKeyWordForm
from django.urls import reverse

TOKEN = os.environ["INVEST_TOKEN"]

class WelcomeScreen(generic.TemplateView):
    template_name = 'parser/welcomeScreen.html'


class SharesListView(generic.ListView):
    queryset = Share.objects.all()
    template_name = 'parser/sharesList.html'
    context_object_name = 'shares'
    paginate_by = 24

    def get_queryset(self):
        if self.request.GET.get('val'):
            value = self.request.GET.get('val')
            queryset = Share.objects.filter(Q(ticker__contains=value) | Q(name__contains=value))
        else:
            queryset = Share.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        val = self.request.GET.get('val')
        context['search'] = val
        return context


def news_table_report(request):
    news_list = News.objects.all().order_by('-pubDate')
    return render(request, 'news_table_report.html', {'news_list': news_list})


def get_tks_shares(request):
    with Client(TOKEN) as client:
        shares = client.instruments.shares()
        # Adding new tickers
        for share in shares.instruments:
            if not Share.objects.filter(ticker=share.ticker).exists():
                db_share = Share(ticker=share.ticker,
                                 figi=share.figi,
                                 class_code=share.class_code,
                                 isin=share.isin,
                                 lot=share.lot,
                                 currency=share.currency,
                                 short_enabled_flag=share.short_enabled_flag,
                                 name=share.name,
                                 exchange=share.exchange,
                                 ipo_date=share.ipo_date,
                                 issue_size=share.issue_size,
                                 country_of_risk=share.country_of_risk,
                                 country_of_risk_name=share.country_of_risk_name,
                                 sector=share.sector,
                                 date_added=datetime.datetime.now()
                                 )
                db_share.save()
                print('Saving new share ticker to db: ' + db_share.ticker)
                messages.add_message(request, messages.INFO, 'New share ticker: ' + db_share.ticker)
        # Deleting tickers which are no longer exist
        db_shares = Share.objects.all()
        for db_share in db_shares:
            db_share_exists = False
            for share in shares.instruments:
                if db_share.ticker == share.ticker:
                    db_share_exists = True
            if not db_share_exists:
                messages.add_message(request, messages.INFO, 'Ticker ' + db_share.ticker + ' deleted')
                db_share.delete()
    messages.add_message(request, messages.SUCCESS, 'TKS invest tickers list updated')
    return redirect('shares_list')


def get_yahoo_ajax_progress_bar_data(request):
    result = get_yahoo_ajax_progress_bar(request)
    return result


def yahoo_parser_news(request):
    parse(request)
    return redirect('news_table_report')


class PreferencesListView(generic.ListView):
    queryset = Preference.objects.all()
    template_name = 'parser/preferencesList.html'
    context_object_name = 'preferences'


class PreferenceCreate(generic.CreateView):
    form_class = PreferenceForm
    template_name = 'parser/preferenceCreate.html'


class NewsKeyWordListView(generic.ListView):
    queryset = NewsKeyWord.objects.all()
    template_name = 'parser/newsKeyWordList.html'
    context_object_name = 'newsKeyWords'
    # paginate_by = 10


class NewsKeyWordsCreate(generic.CreateView):
    form_class = NewsKeyWordForm
    template_name = 'parser/newsKeyWordCreate.html'


class NewsKeyWordsUpdate(generic.UpdateView):
    model = NewsKeyWord
    form_class = NewsKeyWordForm
    template_name = 'parser/newsKeyWordUpdate.html'
    context_object_name = 'news_key_word'


class NewsKeyWordsDelete(generic.DeleteView):
    model = NewsKeyWord
    context_object_name = 'news_key_word'
    template_name = 'parser/newsKeyWordDelete.html'
    success_url = '/news_key_words_list'
