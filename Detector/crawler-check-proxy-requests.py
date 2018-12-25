'''
Check proxy ip - requests version
The program's target is check the proxy is available or not. Because I get proxy for free in web, it maybe cannot use to
crawl.
'''

import requests
import random


header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
                        # ↑ here put the user agent you want to check

'''
The method of write in popular.(If you only one proxy ip)    - line 17
'''
proxy = {'http': 'http://41.190.95.20:39544'}
                # ↑ here put the proxy you want to check, Remember, to clear your proxy is HTTP or HTTPS.


'''
This method be used if you have some amount of proxies    - line 22 to 30
'''
# proxy = '5.39.48.34:443'
# proxy = '192.168.31.7:8080'      # Just write a proxy ip in random, test the program can check or not.
# proxies = {
#     # 'http':'http://' + random.choice(proxy),
#     # # 'https':'https://' + random.choice(proxy)
#     'http': 'http://' + proxy
#     # 'https':'https://' + proxy
# }


'''
We also can wrap up proxy to a function    - line 35 to 42
'''
def get_proxy():
    proxies = [
        '41.190.95.20:39544',
        '114.202.2.185:80'
    ]
    proxy = {
        'http': 'http://' + random.choice(proxies)
        # 'https':'https://' + random.choice(proxies)
    }
    return proxy


'''
Check proxy
'''
try:
    # This web can check some information like what is your header 、 proxy or something else.
    response = requests.get('http://httpbin.org/get', proxies=proxy, headers=header)
    # You also can use random web to check your proxy is available or not.
    # response = requests.get('https://www.youtube.com/?gl=TW&hl=zh-tw', proxies=proxies, headers=header)
    print(response.text)
    print('success')
except requests.exceptions.ConnectionError as e:
    # print('Error:', e.args)
    print('Error : ', e)
except BaseException as e:
    print('Error : Oh no, it\'s fail.......')
    print('\nYour error: ', e)
