from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener, Request



'''測試代理ip - urllib 版本'''

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}

proxy = '5.39.48.34:443'
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    # 'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    # 設定 user agent 也對目標網站發出請求
    request = Request('http://httpbin.org/get', headers=header)
    # 開啟目標網站並設置代理ip proxy
    response = opener.open(request)
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
