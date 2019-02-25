from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import requests
import random
import json
import os



class File:
    def open_file(self, index):
        '''Save text file about the target url we want to crawl the img'''
        img_file_dir = r'D:\DataSource\PycharmProjects\KobeFirstProject\Crawl-1-git-version\crawler_image'
        img_file_path = r'\michael_jordan_' + str(index) + '.png'
        img_path = img_file_dir + img_file_path
        while True:
            try:
                of = open(img_path, 'wb+', encoding='utf-8-sig')
                return of
            except:
                folder = os.path.exists(img_file_dir)
                if not folder:
                    os.mkdir(img_file_dir)
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


    def parser(self, html):
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup


    def parser_pyquery(self, url):
        q = pq(url, headers=self.get_header())
        return q


class Main(Crawler):
    def __init__(self, url):
        self.url = url
        # self.total_page = total_page


    def main_job(self):
        '''This is the main job will work in this program'''
        file_build = File()
        # url = self.url[0] + str(p) + self.url[1]

        '''method 1'''

        html = self.send_request(self.url)
        soup = self.parser(html)
        # print('========This is page ' + str(p) + ' ==========')
        # print(soup)
        # print('==============================================')
        img_row = soup.select('img')
        print(img_row)
        i = 1
        for img_ele in img_row:
            print('test')
            # if len(img_ele) == 0:
            #     print('this is zero')
            #     pass
            # else:
            print(img_ele)
            # print('===========')
            img_attr = img_ele.get('src')
            print(img_attr)
            print('----------')
            img_src = img_ele.get('data-src')
            print(img_src)
            # file = file_build.open_file(i)
            # file.write(img_src)
            # file.close()
            i += 1
            print('The {} picture has downloaded successfully !!! '.format(i))
            print('=====================')

        print('===========Crawler Has Finish===========')

        #     img_src = img_ele.get('src')
        #     print(img_src)

        '''method 2'''

        # q = self.parser_pyquery(self.url)
        # # print(q)
        # q_img = q('img')
        # print(q_img)
        # print(type(q_img))
        # what = q_img
        # print(what)
        # # for i in q_img:
        #     # print(i)
        #     # q_src = i.attr('src')
        #     # print(q_src)


if __name__ == '__main__':
    '''some job'''
    # target_url_head = 'https://www.gettyimages.com/photos/michael-jordan?family=editorial&mediatype=photography&page='
    # target_url_tail = '&phrase=michael%20jordan&sort=mostpopular'
    # target_url = [target_url_head, target_url_tail]
    # target_url = 'https://kenlu.net/2019/02/kicks-on-nba-all-star-game/'
    target_url = 'https://www.google.com/search?q=michael+jordan&source=lnms&tbm=isch&sa=X&sqi=2&ved=0ahUKEwiTkP3_6dPgAhUEdt4KHWp0AmcQ_AUIDigB&biw=1536&bih=722'

    # total_page = 3

    crawler_img = Main(target_url)
    crawler_img.main_job()
