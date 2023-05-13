import requests, re
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup


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


def get_all_finance_calendar_events(request):
    events = []
    url = 'https://www.dailyfx.com/economic-calendar'
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    s.mount(url, HTTPAdapter(max_retries=retries))
    html = s.get(url, headers=HEADERS, timeout=5, params=None)
    if html.status_code == 200:  # success
        pattern = re.compile(r'{"id":"', re.MULTILINE | re.DOTALL)
        # pattern = re.compile(r'.*', re.MULTILINE | re.DOTALL)
        bs_content = BeautifulSoup(html.text, 'html.parser')
        events = bs_content.findAll("script", text=pattern)
        print(events)
        # if script:
        #     print(script)

    return None

