from pyquery import PyQuery as pq
import random



'''測試代理ip - pyquery 版本'''
# https://stackoverflow.com/questions/48756326/web-scraping-results-in-403-forbidden-error/49023958#49023958


def get_header():
    user_agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']
    headers = {'User-Agent': random.choice(user_agent)}
    return headers

def get_proxy():
    proxy = [#'219.76.152.80:80',
             # '47.75.48.149:80',
             # '115.74.227.12:3128'
             '195.64.223.116:3128'
             ]
    proxies = {
        'http': 'http://' + random.choice(proxy),
        # 'https': 'https://' + random.choice(proxy)
    }
    return proxies

proxy = {'http': 'http://77.74.224.37:53081'}

try:
    # q = pq(url='http://httpbin.org/get', proxies=get_proxy(), headers=get_header())
    q = pq(url='http://httpbin.org/get', proxies=proxy, headers=get_header())
    print(q.html())
    print('success !')
except OSError as e:
    print('OSError : ', e)
except:
    print('fuck you error')
