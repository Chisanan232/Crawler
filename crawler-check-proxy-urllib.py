'''
Check proxy ip - urllib version
The program's target is check the proxy is available or not. Because I get proxy for free in web, it maybe cannot use to
crawl.
'''

from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener, Request


header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
                        # ↑ here put the user agent you want to check

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
