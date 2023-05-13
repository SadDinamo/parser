import os
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import edit
from tinkoff.invest import Client
from django.views import generic
from .models import *
from django.contrib import messages
import datetime
from .parsers import *
from .finance_calendar import get_all_finance_calendar_events
from .forms import PreferenceForm, NewsKeyWordForm
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from django.http import JsonResponse
from .tks import *

TOKEN = os.environ['INVEST_TOKEN']


def get_candles(request, figi='BBG001K7WBT8'):
    candle_data = get_5minutes_candles(request, figi)
    return JsonResponse(candle_data, safe=False)


def welcome_screen(request):
    fails_to_deliver = getHtmlNasdaqFailsToDeliverList
    # cnn_fear_and_greed_data = getCnnFearAndGreedStats(request)
    # data = {'fails_to_deliver': fails_to_deliver, 'fear_and_greed': cnn_fear_and_greed_data}
    data = {'fails_to_deliver': fails_to_deliver}
    return render(request, 'parser/welcomeScreen.html', context=data)


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


def news_table_report(request, page=1):
    search_word = request.GET.get('val', '').strip()
    if len(search_word) == 0:
        news_list = News.objects.all().order_by('-pubDate')
    else:
        news_list = News.objects.filter(Q(title__contains=search_word) | Q(description__contains=search_word))
    paginator = Paginator(news_list, 6)
    try:
        news_list = paginator.page(page)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)
    return render(request, 'news_table_report.html', {'news_list': news_list, 'search_word': search_word})


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
                                 date_added=datetime.now()
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


def get_cnn_fear_and_greed_stats(request):
    result = getCnnFearAndGreedStats(request)
    return result


def get_finviz_futures_data(request):
    result = getFinvizFuturesData(request)
    return result


def get_finviz_crypto_data(request):
    result = getFinvizCrypto(request)
    return result


def get_top_news(request):
    news_count = request.POST.get('newsCount', 10)
    top_pub_dates = News.objects.order_by('-pubDate').values()
    result = list(top_pub_dates[:int(news_count)])
    return JsonResponse(result, safe=False)


def get_calendar_events(request):
    events = get_all_finance_calendar_events(request)
    return JsonResponse(events, safe=False)


def launch_news_update_background(request):
    if ServiceVariables.objects.filter(name='yahoo_ticker_update').first().value == 'False':
        parse_jahoo_finance_news_background(request)
    return JsonResponse(1, safe=False)


def get_news_update_status(request):
    result = get_yahoo_ajax_progress_bar(request)
    return result


def get_finviz_top_shorts(request):
    result = getHtmlFinvizTopShorts()
    return JsonResponse(result, safe=False)


def yahoo_parser_news(request):
    parse(request)
    return redirect('news_table_report', page=1)


class PreferencesListView(generic.ListView):
    queryset = Preference.objects.all()
    template_name = 'parser/preferencesList.html'
    context_object_name = 'preferences'


class PreferenceCreate(generic.CreateView):
    form_class = PreferenceForm
    template_name = 'parser/preferenceCreate.html'


class PreferenceUpdate(generic.UpdateView):
    model = Preference
    form_class = PreferenceForm
    template_name = 'parser/preferenceUpdate.html'
    context_object_name = 'preference'


class PreferenceDelete(generic.DeleteView):
    model = Preference
    context_object_name = 'preference'
    template_name = 'parser/preferenceDelete.html'
    success_url = '/preferences'


def check_default_preferencies(request):
    if not Preference.objects.filter(name='YahooNewsHtmlMessageTemplate').first():
        new_preference = Preference()
        new_preference.name = 'YahooNewsHtmlMessageTemplate'
        new_preference.value = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, \'helvetica neue\', helvetica, sans-serif"> <head> <meta charset="UTF-8"> <meta content="width=device-width, initial-scale=1" name="viewport"> <meta name="x-apple-disable-message-reformatting"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta content="telephone=no" name="format-detection"> <title>письмо с новостью</title><!--[if (mso 16)]> <style type="text/css"> a {text-decoration: none;} </style> <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]><xml> <o:OfficeDocumentSettings> <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings></xml><![endif]--> <style type="text/css">#outlook a {	padding:0;}.es-button {	mso-style-priority:100!important;	text-decoration:none!important;}a[x-apple-data-detectors] {	color:inherit!important;	text-decoration:none!important;	font-size:inherit!important;	font-family:inherit!important;	font-weight:inherit!important;	line-height:inherit!important;}.es-desk-hidden {	display:none;	float:left;	overflow:hidden;	width:0;	max-height:0;	line-height:0;	mso-hide:all;}[data-ogsb] .es-button {	border-width:0!important;	padding:10px 20px 10px 20px!important;}@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:30px!important; text-align:left } h2 { font-size:24px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:30px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:24px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:inline-block!important } a.es-button, button.es-button { font-size:18px!important; display:inline-block!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } }</style> </head> <body style="width:100%;font-family:arial, \'helvetica neue\', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"> <div class="es-wrapper-color" style="background-color:#F6F6F6"><!--[if gte mso 9]>			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">				<v:fill type="tile" color="#f6f6f6"></v:fill>			</v:background>		<![endif]--> <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"> <tr> <td valign="top" style="padding:0;Margin:0"> <table class="es-header" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top"> <tr> <td align="center" style="padding:0;Margin:0"> <table class="es-header-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" style="padding:0;Margin:0"><h2 style="Margin:0;line-height:29px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:24px;font-style:normal;font-weight:normal;color:#333333">\'+new_news_item.title+\'</h2></td> </tr> </table></td> </tr> </table></td> </tr> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:21px;color:#333333;font-size:14px">\'+new_news_item.pubDate+\'</p></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table> <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> <tr> <td align="center" style="padding:0;Margin:0"> <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td class="es-m-txt-l" style="padding:0;Margin:0;padding-left:10px;padding-right:10px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:17px;color:#333333;font-size:14px;text-align:justify">\'+new_news_item.description+\'</p></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table> <table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top"> <tr> <td align="center" style="padding:0;Margin:0"> <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" style="padding:0;Margin:0"><span class="es-button-border" style="border-style:solid;border-color:#2cb543;background:#93c47d;border-width:0px;display:block;border-radius:15px;width:auto"><a href="\'+new_news_item.link+\'" class="es-button" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#38761d;font-size:18px;border-style:solid;border-color:#93c47d;border-width:10px 20px 10px 20px;display:block;background:#93c47d;border-radius:15px;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-weight:normal;font-style:normal;line-height:22px;width:auto;text-align:center;border-left-width:5px;border-right-width:5px">Читать в источнике</a></span></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table> </div> </body></html>'
        new_preference.default_value = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, \'helvetica neue\', helvetica, sans-serif"> <head> <meta charset="UTF-8"> <meta content="width=device-width, initial-scale=1" name="viewport"> <meta name="x-apple-disable-message-reformatting"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta content="telephone=no" name="format-detection"> <title>письмо с новостью</title><!--[if (mso 16)]> <style type="text/css"> a {text-decoration: none;} </style> <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]><xml> <o:OfficeDocumentSettings> <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings></xml><![endif]--> <style type="text/css">#outlook a {	padding:0;}.es-button {	mso-style-priority:100!important;	text-decoration:none!important;}a[x-apple-data-detectors] {	color:inherit!important;	text-decoration:none!important;	font-size:inherit!important;	font-family:inherit!important;	font-weight:inherit!important;	line-height:inherit!important;}.es-desk-hidden {	display:none;	float:left;	overflow:hidden;	width:0;	max-height:0;	line-height:0;	mso-hide:all;}[data-ogsb] .es-button {	border-width:0!important;	padding:10px 20px 10px 20px!important;}@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:30px!important; text-align:left } h2 { font-size:24px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:30px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:24px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:inline-block!important } a.es-button, button.es-button { font-size:18px!important; display:inline-block!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } }</style> </head> <body style="width:100%;font-family:arial, \'helvetica neue\', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"> <div class="es-wrapper-color" style="background-color:#F6F6F6"><!--[if gte mso 9]>			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">				<v:fill type="tile" color="#f6f6f6"></v:fill>			</v:background>		<![endif]--> <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"> <tr> <td valign="top" style="padding:0;Margin:0"> <table class="es-header" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top"> <tr> <td align="center" style="padding:0;Margin:0"> <table class="es-header-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" style="padding:0;Margin:0"><h2 style="Margin:0;line-height:29px;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-size:24px;font-style:normal;font-weight:normal;color:#333333">\'+new_news_item.title+\'</h2></td> </tr> </table></td> </tr> </table></td> </tr> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:21px;color:#333333;font-size:14px">\'+new_news_item.pubDate+\'</p></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table> <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> <tr> <td align="center" style="padding:0;Margin:0"> <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td class="es-m-txt-l" style="padding:0;Margin:0;padding-left:10px;padding-right:10px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, \'helvetica neue\', helvetica, sans-serif;line-height:17px;color:#333333;font-size:14px;text-align:justify">\'+new_news_item.description+\'</p></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table> <table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top"> <tr> <td align="center" style="padding:0;Margin:0"> <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px"> <tr> <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px"> <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" valign="top" style="padding:0;Margin:0;width:560px"> <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> <tr> <td align="center" style="padding:0;Margin:0"><span class="es-button-border" style="border-style:solid;border-color:#2cb543;background:#93c47d;border-width:0px;display:block;border-radius:15px;width:auto"><a href="\'+new_news_item.link+\'" class="es-button" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#38761d;font-size:18px;border-style:solid;border-color:#93c47d;border-width:10px 20px 10px 20px;display:block;background:#93c47d;border-radius:15px;font-family:arial, \'helvetica neue\', helvetica, sans-serif;font-weight:normal;font-style:normal;line-height:22px;width:auto;text-align:center;border-left-width:5px;border-right-width:5px">Читать в источнике</a></span></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table></td> </tr> </table> </div> </body></html>'
        new_preference.description = 'Template used to send filtered news via e-mail. \n'\
                                     'Use \'+new_news_item.title+\'  \'+new_news_item.pubDate+\'  ' \
                                     '\'+new_news_item.description+\'  \'+new_news_item.link+\''
        new_preference.save()

    if not ServiceVariables.objects.filter(name='current_ticker_counter').first():
        new_ServiceVariable = ServiceVariables()
        new_ServiceVariable.name = 'current_ticker_counter'
        new_ServiceVariable.value = ''
        new_ServiceVariable.save()

    if not ServiceVariables.objects.filter(name='total_tickers').first():
        new_ServiceVariable = ServiceVariables()
        new_ServiceVariable.name = 'total_tickers'
        new_ServiceVariable.value = ''
        new_ServiceVariable.save()

    if not ServiceVariables.objects.filter(name='ticker_name').first():
        new_ServiceVariable = ServiceVariables()
        new_ServiceVariable.name = 'ticker_name'
        new_ServiceVariable.value = ''
        new_ServiceVariable.save()

    if not ServiceVariables.objects.filter(name='yahoo_ticker_update').first():
        new_ServiceVariable = ServiceVariables()
        new_ServiceVariable.name = 'yahoo_ticker_update'
        new_ServiceVariable.value = ''
        new_ServiceVariable.save()

    return redirect('preferences')


def reset_to_defaults(request):
    preferences = Preference.objects.all()
    for pref in preferences:
        if pref.default_value != None and pref.default_value != '':
            pref.value = pref.default_value
            pref.save()
    if ServiceVariables.objects.filter(name='yahoo_ticker_update').first():
        ServiceVariable = ServiceVariables.objects.filter(name='yahoo_ticker_update').first()
        ServiceVariable.value = 'False'
        ServiceVariable.save()
    return redirect('preferences')


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


def ttest(request):
    with Client(TOKEN) as client:
        accounts = client.users.get_accounts()
        account = accounts.accounts[0]
        temp_data = client.operations.get_portfolio(account_id=account.id)
        print(temp_data)
    return redirect('welcome_screen')
