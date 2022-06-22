from django.urls import path
from django.http import HttpResponse
from .views import *
from .models import *


urlpatterns = [
    path('', WelcomeScreen.as_view(), name='welcome_screen'),
    path('shareslist', SharesListView.as_view(), name='shares_list'),
    path('welcome', WelcomeScreen.as_view(), name='welcome_screen'),
    path('get_tks_shares',  get_tks_shares, name='get_tks_shares'),
    path('yahoo_parser_news', yahoo_parser_news, name='yahoo_parser_news'),
    path('news_table_report', news_table_report, name='news_table_report'),
    path('get_yahoo_ajax_progress_bar_data', get_yahoo_ajax_progress_bar_data, name='get_yahoo_ajax_progress_bar_data'),
    path('preferences', PreferencesListView.as_view(), name='preferences'),
    path('pref_modal_save', PreferenceModalFormCreate.as_view(), name='pref_modal_save'),
    path('news_key_words_list', NewsKeyWordListView.as_view(), name='news_key_words_list'),
    path('news_key_words_create', NewsKeyWordsCreate.as_view(), name='news_key_words_create'),
    path('news_key_words_update/<int:pk>', NewsKeyWordsUpdate.as_view(), name='news_key_words_update'),
    path('news_key_words_delete/<int:pk>', NewsKeyWordsDelete.as_view(), name='news_key_words_delete'),
]

