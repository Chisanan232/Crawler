from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import requests
import random
import os
import re



class File:
    def open_file(self, index):
        video_file_dir = r'D:\DataSource\PycharmProjects\KobeFirstProject\Crawl-1-git-version\crawler_result_data\crawler_video'
        video_file_path = r'\michael_jordan_' + str(index) + '.wmv'
        video_file = video_file_dir + video_file_path
        while True:
            try:
                of = open(video_file, 'wb')
                return of
            except:
                folder = os.path.exists(video_file_dir)
                if not folder:
                    os.mkdir(video_file_dir)
                else:
                    pass


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


class Crawler(Protect):
    def send_request(self, url):
        html = requests.get(url, headers=self.get_header())
        return html


    def parser(self, html, file_build):
        soup = BeautifulSoup(html.text, 'html.parser')
        video_row = soup.select('a')
        for video in video_row:
            video_ele = video.get('href')
            match_ele = re.search('watch.v=(.*)', video_ele).group(0)
            if not match_ele:
                pass
            else:
                print(match_ele)
                video_url = 'https://youtube.com/' + match_ele
                video_html = requests.get(video_url)
                video_bin = video_html.content



    def parser_pyquery(self, url):
        q = pq(url, headers=self.get_header())
        return q


class Main(Crawler):
    def __init__(self, url):
        self.url = url


    def main_job(self):
        file_build = File()

        html = self.send_request(self.url)
        self.parser(html, file_build)

        print('==========Crawler Has Finish============')


if __name__ == '__main__':
    '''something you want to do'''
    target_url = 'https://www.youtube.com/results?search_query=michael+jordan'

    crawler_video = Main(target_url)
    crawler_video.main_job()
