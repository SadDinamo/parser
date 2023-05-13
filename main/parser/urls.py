from django.urls import path
from django.http import HttpResponse
from .views import *
from .models import *


urlpatterns = [
    path('', welcome_screen, name='welcome_screen'),
    path('shareslist', SharesListView.as_view(), name='shares_list'),
    path('welcome', welcome_screen, name='welcome_screen'),
    path('get_tks_shares',  get_tks_shares, name='get_tks_shares'),
    path('yahoo_parser_news', yahoo_parser_news, name='yahoo_parser_news'),
    path('news_table_report/<int:page>/', news_table_report, name='news_table_report'),
    path('get_yahoo_ajax_progress_bar_data', get_yahoo_ajax_progress_bar_data, name='get_yahoo_ajax_progress_bar_data'),
    path('preferences', PreferencesListView.as_view(), name='preferences'),
    path('preference_create', PreferenceCreate.as_view(), name='preference_create'),
    path('preference_update/<int:pk>/', PreferenceUpdate.as_view(), name='preference_update'),
    path('preference_delete/<int:pk>/', PreferenceDelete.as_view(), name='preference_delete'),
    path('preference_check_default', check_default_preferencies, name='preference_check_default'),
    path('preferences_reset_to_defaults', reset_to_defaults, name='preferences_reset_to_defaults'),
    path('news_key_words_list', NewsKeyWordListView.as_view(), name='news_key_words_list'),
    path('news_key_words_create', NewsKeyWordsCreate.as_view(), name='news_key_words_create'),
    path('news_key_words_update/<int:pk>/', NewsKeyWordsUpdate.as_view(), name='news_key_words_update'),
    path('news_key_words_delete/<int:pk>/', NewsKeyWordsDelete.as_view(), name='news_key_words_delete'),
    path('get_cnn_fear_and_greed_stats', get_cnn_fear_and_greed_stats, name='get_cnn_fear_and_greed_stats'),
    path('get_finviz_futures_data', get_finviz_futures_data, name='get_finviz_futures_data'),
    path('get_finviz_crypto_data', get_finviz_crypto_data, name='get_finviz_crypto_data'),
    path('get_top_news', get_top_news, name='get_top_news'),
    path('get_news_update_status', get_news_update_status, name='get_news_update_status'),
    path('launch_news_update_background', launch_news_update_background, name='launch_news_update_background'),
    path('get_top_shorts', get_finviz_top_shorts, name='get_top_shorts'),
    path('get_candles', get_candles, name='get_candles'),
    path('get_calendar_events', get_calendar_events, name='get_calendar_events'),
    path('ttest',  ttest, name='ttest'),
]

