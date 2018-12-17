import requests
import random



'''測試代理ip - requests 版本'''

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}

# 一般寫法(只有一個代理ip的情況下)
proxy = 'http://217.61.125.74:3128'

# # 有多個代理能使用的情況
# proxy = '5.39.48.34:443'
# proxy = '192.168.31.7:8080'     # 隨機打的ip測試是否真的能檢驗ip

proxies = {
    # 'http':'http://' + random.choice(proxy),
    # # 'https':'https://' + random.choice(proxy)
    'http': 'http://' + proxy,
    # 'https':'https://' + proxy
}

# 將代理ip包裝成函數
def get_proxy():

    proxy = ['140.227.75.216:3128', '114.202.2.185:80']
    proxies = {
        'http':'http://' + random.choice(proxy),
        # 'https':'https://' + random.choice(proxy)
    }
    return proxies

# 測試代理ip
try:
    response = requests.get('http://httpbin.org/get', proxies=proxy, headers=header)
    # response = requests.get('https://www.youtube.com/?gl=TW&hl=zh-tw', proxies=proxies, headers=header)
    print(response.text)
    print('success')
except requests.exceptions.ConnectionError as e:
    # print('Error:', e.args)
    print('Error : ', e)
except:
    print('Error : fuck you')
