from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import requests
import random
import os



class Protect:
    def get_header(self):
        '''The setting about set header to hide identification itself'''
        user_agent = [
            # Apple iPhone 7 Plus
            'Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
            # Windows 10-based PC using Edge browser
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            # Mac OS X-based computer using a Safari browser
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            # Linux-based PC using a Firefox browser
            'Linux-based PC using a Firefox browser',
            # Windows User Agents
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Mwendo/1.1.5 Safari/537.21'
        ]
        header = {'User-Agent': random.choice(user_agent)}
        return header


    def get_proxy(self):
        '''The setting about set proxy to prevent about be block by web server'''
        proxies_pool = [
            'http://58.11.72.35:3128',
            'http://77.74.224.37:53081',
            'http://103.24.110.21:39689',
            'http://118.174.65.137:54063',
            'http://203.151.50.213:3128',
            'http://95.87.202.118:80',
            'http://217.196.64.201:50885	',
        ]
        proxy = {
            'http': 'http://' + random.choice(proxies_pool),
            'https': 'https://' + random.choice(proxies_pool)
        }
        return proxy


class Crawler:
    def parser(self, url):
        html = requests.get(url)
        return html


    def parser_pyquery(self, url):
        q = pq(url)
        return q


if __name__ == '__main__':
    '''something you want to do'''
