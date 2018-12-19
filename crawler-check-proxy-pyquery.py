'''
Check proxy ip - pyquery version
The program's target is check the proxy is available or not. Because I get proxy for free in web, it maybe cannot use to
crawl.
'''

from pyquery import PyQuery as pq
import random

# https://stackoverflow.com/questions/48756326/web-scraping-results-in-403-forbidden-error/49023958#49023958

'''
Wrap up get one of headers or get one of proxies in random to a function.
'''
def get_header():
    user_agent = [
        'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
    ]
    headers = {'User-Agent': random.choice(user_agent)}
    return headers


def get_proxy():
    proxy = [
        #'219.76.152.80:80',
        # '47.75.48.149:80',
        # '115.74.227.12:3128',
        '41.190.95.20:39544'
             ]
    proxies = {
        'http': 'http://' + random.choice(proxy)
        # 'https': 'https://' + random.choice(proxy)
    }
    return proxies


try:
    q = pq(url='http://httpbin.org/get', proxies=get_proxy(), headers=get_header())
    print(q.html())
    print('success !')
except OSError as e:
    print('OSError : ', e)
except BaseException as e:
    print('Error : Oh no, it\'s fail.......')
    print('\nYour error: ', e)

