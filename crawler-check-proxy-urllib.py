'''
Check proxy ip - urllib version
The program's target is check the proxy is available or not. Because I get proxy for free in web, it maybe cannot use to
crawl.
'''

from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener, Request
import random


header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
                        # ↑ here put the user agent you want to check


def get_header():
    user_agent = [
        # sang sung
        'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
        # sony
        'Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
        # apple iphone
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'
                  ]
    headers = {'User-Agent': random.choice(user_agent)}
    return headers


proxy = '41.190.95.20:39544'
# ↑ here put the proxy you want to check, Remember, to clear your proxy is HTTP or HTTPS.

proxy_handler = ProxyHandler({
    'http': 'http://' + proxy
    # 'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    # Setting user agent and send requests to target web.
    request = Request('http://httpbin.org/get', headers=header)
    # Open target web and setting proxy ip
    response = opener.open(request)
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
