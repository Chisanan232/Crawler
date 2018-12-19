from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from tomorrow import threads
import requests
import random
import time
import csv
import sys
import os



class DefineParameter:
    def __init__(self, save_path, year_initial, year_conclude):
        self.path = save_path
        self.year_initial = year_initial
        self.year_conclude = year_conclude


class FakeIdentity:
    def get_header(self):
        user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
        ]
        headers = {'User-Agent': random.choice(user_agent)}
        return headers


    def get_proxy(self):
        proxy = ['217.61.125.74:3128',
                 '118.178.93.238:8888',
                 '212.237.15.108:8080',
                 '206.189.220.129:8080',
                 '114.202.2.185:80',
                 '206.189.222.146:8080',
                 '66.119.180.104:80',
                 '187.73.68.14:53281',
                 '194.126.183.141:53281',
                 '95.167.109.76:80',
                 '167.99.235.224:80',
                 '27.255.91.146:80',
                 '47.89.241.103:8080',
                 '47.52.208.159:80',
                 '213.155.250.46:3128',
                 ]
        proxies = {
            'http': 'http://' + random.choice(proxy)
            # Hyper Text Transfer Protocol (HTTP) cannot use carelessly, to remember, HTTP and HTTPS look similar but
            # they are different at all. Here, we have to pay attention to sure your proxy is HTTP or HTTPS. If you want
            # to study more information about http and https, please google.
            # http://blog.51cto.com/laoyinga/2046692
            # 'https':'https://' + random.choice(proxy)
        }
        return proxies


class AllUrlInWorker(DefineParameter):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(AllUrlInWorker, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)
        self.address = address

    '''
    Collect all of urls that we will crawl to get data we want
    '''

    def get_url(self, year_start, year_end, month_start, month_end, day_start, day_end):
        url_address = self.address
        url_head = 'https://www.timeanddate.com/scripts/cityajax.php?n=usa/'
        url_mid = '&mode=historic&hd='
        url_mid_two = '&month='
        url_tail = '&year='

        '''
        A method save urls string we need with for loop.
        First method to get all urls we want to crawl, just use nested for loop. Because we just collect all urls, it's 
        string in list, so we don't consider some problems about efficiency.
        '''
        url_pool = []
        date_list = []

        for year in range(year_start, year_end):
            for month in range(month_start, month_end):
                m = '%02d' % month
                for day in range(day_start, day_end):
                    d = '%02d' % day
                    url = url_head + url_address + url_mid + str(year) + m.zfill(2) + d.zfill(2) + \
                          url_mid_two + str(month) + url_tail + str(year)
                    url_pool.append(url)
                    # date = str(year) + m.zfill(2) + d.zfill(2)
                    date = str(year) + '/' + str(m.zfill(2)) + '/' + str(d.zfill(2))
                    date_list.append(date)
        '''
        Second method save urls string we need with for loop too, but wrote it by 'Python method'.
        It\'s so abnormal, even thought it\'s convenience but it\'s so hard to read and understand what you want to do.
        '''
        # url_pool = [(url_head + url_address + url_mid + str(year) + str(('%02d' % month).zfill(2)) +
        #             str(('%02d' % day).zfill(2)) + url_mid_two + str(month) + url_tail + str(year))
        #             for year in range(year_start, year_end) for month in range(month_start, month_end)
        #             for day in range(day_start, day_end)]
        # date_list = [(str(year) + str(('%02d' % month).zfill(2)) + str(('%02d' % day).zfill(2)))
        #              for year in range(year_start, year_end) for month in range(month_start, month_end)
        #              for day in range(day_start, day_end)]
        return url_pool, date_list


'''
I try to use 3 methods about 1、120 and 240 threads to crawl data, so I will write three classes to cooperate with different 
number of threads.
'''


class PrepositiveMeasureVerOne(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerOne, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude, address=address)

    '''
    This method is applicable to crawl 1 year data
    '''

    def get_job_date(self, name):

        '''
        A method to get url let every worker to do something they should to do
        '''

        # if name == 'worker-no-0':
        #     url_pool, date_list = self.get_url(2013, 2014, 1, 3, 1, 32)
        #     return url_pool, date_list
        # elif name == 'worker-no-1':
        #     url_pool, date_list = self.get_url(2013, 2014, 3, 6, 1, 32)
        #     return url_pool, date_list
        # elif name == 'worker-no-2':
        #     url_pool, date_list = self.get_url(2013, 2014, 5, 7, 1, 32)
        #     return url_pool, date_list
        # elif name == 'worker-no-3':
        #     url_pool, date_list = self.get_url(2013, 2014, 7, 9, 1, 32)
        #     return url_pool, date_list
        # elif name == 'worker-no-4':
        #     url_pool, date_list = self.get_url(2013, 2014, 9, 11, 1, 32)
        #     return url_pool, date_list
        # elif name == 'worker-no-5':
        #     url_pool, date_list = self.get_url(2013, 2014, 11, 13, 1, 32)
        #     return url_pool, date_list
        # else:
        #     print('Not found this worker name.')
        '''
        Second method
        '''
        if name[-3:].isdigit():
            month_begin = 1 + 1 * int(name[-3:])
            month_finish = 2 + 1 * int(name[-3:])
            url_pool, date_list = self.get_url(self.year_initial, self.year_conclude, month_begin, month_finish, 1, 32)
            return url_pool, date_list
        else:
            print('Please check your name of variable \'worker\', the last 3 string is not integer.')
            ans = input('Do you want to stop the program ? (Yes/No)')
            if 'y' in ans or 'Y' in ans:
                sys.exit()
            else:
                print('Program keep operating.')

    def open_file(self, worker):
        file = self.path + str(self.year_initial) + '/weather-' + str(int(int(worker[-3:]) % 12) + 1) + '.csv'
        csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
        write_file = csv.writer(csv_file)
        return csv_file, write_file


class PrepositiveMeasureVerTwo(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerTwo, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude, address=address)

    '''
    Second method, we want to get ten years data in one time.
    '''

    def get_job_date(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 12)
            arg_month = int(worker[-3:]) % 12
            month_begin = 1 + 1 * arg_month
            month_finish = 2 + 1 * arg_month
            year_begin = self.year_initial + 1 * mul
            year_finish = self.year_conclude + 1 * mul
            url_pool, date_list = self.get_url(year_begin, year_finish, month_begin, month_finish, 1, 32)
            return url_pool, date_list
        else:
            print('Please check your name of variable \'worker\', the last 3 string is not integer.')
            ans = input('Do you want to stop the program ? (Yes/No)')
            if 'y' in ans or 'Y' in ans:
                sys.exit()
            else:
                print('Program keep operating.')

    '''
    This function aim to get ten years data in one time
    '''

    def open_file(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 12)
            year = self.year_initial + 1 * mul
            file = self.path + str(year) + '/weather-' + str(int(int(worker[-3:]) % 12) + 1) + '-month.csv'
            csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
            write_file = csv.writer(csv_file)
            return csv_file, write_file
        else:
            print('Please check your name of variable \'worker\', the last 3 string is not integer.')
            ans = input('Do you want to stop the program ? (Yes/No)')
            if 'y' in ans or 'Y' in ans:
                sys.exit()
            else:
                print('Program keep operating.')


class PrepositiveMeasureVerThree(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerThree, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude, address=address)

    '''
    Third method, we want to use more threads to get ten years data in one time.
    '''

    '''
    Question : Is it better? More faster?
    Answer 1 :  We crawl from 2009 to 2011 about 2 years and 1 month, took 16.278 seconds
    Answer 2 : We crawl from 2009 to 2013 about 4 years and 1 month, took 30.092 seconds
    Answer 3 : We crawl from 2013 to 2017 about 4 years, took 36.027 seconds
    we can pay attention to the average time of it spend in all time, unfortunately, it is a little slower than the
    situation that we use less threads
    '''

    def get_job_date(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 24)
            arg_month = int(worker[-3:]) % 24
            if arg_month < 12:
                day_begin = 1
                day_finish = 17
                month_begin = 1 + 1 * arg_month
                month_finish = 2 + 1 * arg_month
            else:
                new_arg_month = arg_month - 12
                day_begin = 17
                day_finish = 32
                month_begin = 1 + 1 * new_arg_month
                month_finish = 2 + 1 * new_arg_month
            year_begin = self.year_initial + 1 * mul
            year_finish = self.year_conclude + 1 * mul
            url_pool, date_list = self.get_url(year_begin, year_finish, month_begin, month_finish, day_begin,
                                               day_finish)
            return url_pool, date_list
        else:
            print('Please check your name of variable \'worker\', the last 3 string is not integer.')
            ans = input('Do you want to stop the program ? (Yes/No)')
            if 'y' in ans or 'Y' in ans:
                sys.exit()
            else:
                print('Program keep operating.')


    def open_file(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 24)
            year = self.year_initial + 1 * mul
            if int(int(worker[-3:]) % 24) < 12:
                file = self.path + str(year) + '/weather-' + str(
                    int(int(worker[-3:]) % 24) + 1) + '-month-first-two-weeks.csv'
                csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
                write_file = csv.writer(csv_file)
                return csv_file, write_file
            else:
                file = self.path + str(year) + '/weather-' + str(
                    int(int(worker[-3:]) % 24) - 11) + '-month-second-two-weeks.csv'
                csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
                write_file = csv.writer(csv_file)
                return csv_file, write_file
        else:
            print('Please check your name of variable \'worker\', the last 3 string is not integer.')
            ans = input('Do you want to stop the program ? (Yes/No)')
            if 'y' in ans or 'Y' in ans:
                sys.exit()
            else:
                print('Program keep operating.')


class BsCrawler(FakeIdentity, PrepositiveMeasureVerTwo):
    def parser(self, target_url_pool, date_list, write_in_file, worker):
        index = 0
        for url in target_url_pool:
            html = requests.get(url, headers=self.get_header())
            if html.status_code == requests.codes.ok:
                soup = BeautifulSoup(html.text, 'html.parser')
                web_data = soup.select('tbody > tr')[0].text
                if web_data == 'No data available for the given date. Try selecting a different day.':
                    print('-------------------------')
                    print('There is nothing in this data.')
                    print('-------------------------')
                    for date in date_list:
                        if date in url:
                            date_list.remove(date)
                    pass
                else:
                    tableRow = soup.select('tbody > tr')
                    for row in tableRow:
                        Time = row.select_one('th').text
                        # Time = row.select('th')[0].text
                        newTime = Time[0:5]
                        weather = row.select('.mtt')[0].get('title')
                        Temp = row.select_one('.wt-ic + td').text
                        wind = row.select('.sep')[0].text
                        Barometer = row.select('.sep')[1].text
                        wind_dir = row.select('.comp')[0].get('title')
                        Bar = row.select('.sep')[1]
                        Humidity = Bar.find_previous_siblings('td')[0].text
                        Bar = row.select('.sep')[1]
                        Visibility = Bar.find_next_siblings('td')[0].text

                        Temp1 = "".join(Temp.split())
                        Visibility1 = "".join(Visibility.split())

                        nws = [newTime, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1]
                        nws.insert(0, date_list[index])
                        write_in_file.writerow(nws)
                        # time.sleep(random.randint(random.randint(1, 4) + random.randint(2, 3), random.randint(4, 13) + random.randint(4, 7)))
                    index += 1
                    if index == 1:
                        print('The data of ' + str(index) + 'st day has been recorded success ! - ' + str(worker))
                    elif index == 2:
                        print('The data of ' + str(index) + 'nd day has been recorded success ! - ' + str(worker))
                    elif index == 3:
                        print('The data of ' + str(index) + 'rd day has been recorded success ! - ' + str(worker))
                    else:
                        print('The data of ' + str(index) + 'th day has been recorded success ! - ' + str(worker))


    @threads(120)
    def main_job(self, worker):
        crawl_start_time = time.time()
        fields = ['Date', 'Time', 'Weather', 'Temperature', 'Wind', 'Wind Direction', 'Humidity', 'Barometer', 'Visibility']
        csv_file, write_file = self.open_file(worker)
        write_file.writerow(fields)
        url_pool, date_list = self.get_job_date(worker)
        self.parser(url_pool, date_list, write_file, worker)
        csv_file.close()
        crawl_end_time = time.time()
        print('------------------------')
        print('Total time: ' + str(crawl_end_time - crawl_start_time) + ' seconds. - ' + str(worker))
        print('Crawler Finish. - ' + str(worker))
        print('------------------------')


if __name__ == '__main__':
    print('Program start.')

    threads_num = 120       # You can change 120 to 1 or 240 to observe the results. And remember, if you alter,besides
                            # you should to alter the number of lebal in line 341, you have to alter class BsCrawler
                            # inherit from which one of class.
    year_start = 2009       # You can change to the year you want to crawl
    year_end = 2010
    crawl_address = 'san-jose'    # The data of weather in address where you want to crawl.
    path = 'The path where you want to save data'

    '''
    Check the path is exit or not, if not, then build it.
    '''
    for year in range(year_start, year_start + int(threads_num / 12)):
        folder = os.path.exists(path + str(year) + '/')
        if not folder:
            os.makedirs(path + str(year) + '/')
            print(path + str(year) + '/')
            print('Build folder success !!!')

    bs_crawler = BsCrawler(save_path=path, year_initial=year_start, year_conclude=year_end, address=crawl_address)

    workers_list = [('worker-' + str('%003d' % num)) for num in range(threads_num)]
    for j in workers_list:
        bs_crawler.main_job(j)

    print('finish')
