from bs4 import BeautifulSoup
import requests
import json



class File:
    def open_file(self):
        '''Save text file about the target url we want to crawl the img'''
        title_list = r'D:\DataSource\PycharmProjects\KobeFirstProject\Crawl-1-git-version\crawler_img_title_list.txt'
        of = open(title_list, encoding='utf-8-sig')
        return of


class Project:
    def get_header(self):
        '''The setting about set header to hide identification itself'''


    def get_proxy(self):
        '''The setting about set proxy to prevent about be block by web server'''


class Crawler:
    def request(self, url):
        html = requests.get(url)
        return html


class Main(Crawler):
    def main_job(self):
        '''This is the main job will work in this program'''


if __name__ == '__main__':
    '''some job'''
