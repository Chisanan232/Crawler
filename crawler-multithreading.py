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
        user_agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                      'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393']
        headers = {'User-Agent':random.choice(user_agent)}
        return headers


    def get_proxy(self):
        proxy = ['217.61.125.74:3128',
                 '118.178.93.238:8888',
                 '212.237.15.108:8080',
                 '206.189.220.129:8080',
                 '114.202.2.185:80',
                 '206.189.222.146:8080',
                 '66.119.180.104:80',
                 '187.73.68.14:53281',     # super hide
                 '194.126.183.141:53281',    # super hide
                 '95.167.109.76:80',      # super hide
                 '167.99.235.224:80',     # super hide
                 '27.255.91.146:80',
                 '47.89.241.103:8080',
                 '47.52.208.159:80',     #super hide
                 '213.155.250.46:3128',
                 '47.52.61.16:80',
                 '47.91.156.171:80',
                 '210.1.58.213:8080',
                 '202.166.117.46:8080',
                 '140.227.75.216:3128',   #super hide
                 '190.214.26.90:53281',   #super hide
                 '82.67.50.98:80',
                 '91.185.21.238:8080',
                 '148.243.240.156:53281',   #super hide
                 '43.228.126.175:80',    #super hide
                 '140.227.73.204:3128',   #super hide
                 '138.197.165.71:3128',
                 '93.187.167.54:3128',    #super hide
                 '202.166.117.46:8080',
                 '47.75.101.170:80',
                 '5.39.48.34:80',     #super hide
                 '189.8.68.78:3128',
                 '200.255.122.174:8080',
                 '66.70.166.200:80',      #super hide
                 '153.149.169.215:3128',       #super hide
                 '181.129.183.19:53281',     #super hide
                 '142.93.251.113:80',
                 '178.128.176.221:3128',
                 '217.61.125.74:3128',
                 '119.28.179.87:8080',
                 '213.136.87.65:80',
                 '119.28.37.58:80',
                 '177.67.83.134:80',
                 '90.110.13.100:80',     #super hide
                 '142.93.58.158:3128',
                 '178.128.64.241:3128',
                 '142.93.11.154:8080',
                 '41.222.226.46:80',
                 '167.114.47.173:80',
                 '181.49.24.126:8081',
                 '212.83.164.85:80',    #super hide      #50
                 '178.128.176.221:8080',
                 '203.77.239.5:53281',   #super hide
                 '47.91.237.251:80',
                 '122.155.166.193:80',   #super hide
                 '139.59.81.158:80',   #super hide
                 '140.227.60.114:3128',   #super hide
                 '217.61.125.74:8080',
                 '80.211.170.159:80',
                 '110.232.86.52:53281',    #super hide
                 '113.53.54.213:42259',     #super hide
                 '158.69.243.155:8888',
                 '171.255.199.129:80',
                 '115.126.86.168:8090',
                 '142.93.250.239:80',
                 '202.21.32.148:8080',     #super hide
                 '47.75.48.149:80',
                 '206.189.220.129:80',
                 '217.61.125.74:8080',
                 '142.93.51.159:80',
                 '150.163.105.2:8080',    #super hide
                 '163.172.173.187:3000',
                 '178.128.64.241:8080',
                 '115.74.227.12:3128',     #super hide
                 '181.129.183.19:53281',    #super hide
                 '167.114.167.143:32231',    #super hide
                 '85.237.167.120:41258',    #super hide
                 '35.185.201.225:8080',    #super hide
                 '80.211.170.159:80',
                 '66.70.173.54:80',
                 '138.197.165.71:3128',
                 '47.90.87.225:88',                 #81
                 '113.53.54.213:42259',     #super hide
                 '204.48.22.246:8080',
                 '190.52.198.153:3128',    #super hide
                 '153.149.169.64:3128',   #super hide
                 '167.99.235.224:80',     #super hide
                 '142.93.251.113:80',
                 '182.23.45.147:53281',
                 '47.52.153.167:443',
                 '203.78.141.118:8080',
                 '47.52.64.149:80',
                 '81.17.17.163:80',
                 '177.66.63.225:21776',    #super hide
                 '142.93.247.178:3128',
                 '190.152.182.150:53281',    #super hide
                 '47.91.237.251:80',
                 '54.39.98.138:8080',
                 '119.28.21.144:8080',
                 '140.227.81.53:3128',    #super hide
                 '27.116.51.21:32231',    #super hide
                 '108.61.186.207:8080',
                 '66.70.166.200:80',    #super hide
                 '90.110.13.100:80',    #super hide
                 '128.140.225.41:80',    #super hide
                 '2.44.120.195:41258',    #super hide
                 '93.58.124.32:80',
                 '5.39.48.34:443',    #super hide
                 '47.52.209.8:80',
                 '110.232.86.52:53281',    #super hide
                 '142.93.11.154:8080',
                 '219.76.152.80:80'     #111 proxies
                 ]
        proxies = {
            'http':'http://' + random.choice(proxy),
            # hyper超文本傳輸協定http不可亂使用，要切記http跟https雖然很像但是是完全不一樣不能夠混用的，
            # 在使用代理ip(proxy)時，要確認此代理ip的協定是http還是https。If you want to study more
            # information about http and https, please google nigga.
            # http://blog.51cto.com/laoyinga/2046692
            # 'https':'https://' + random.choice(proxy)
        }
        return proxies


class AllUrlInWorker(DefineParameter):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(AllUrlInWorker, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)
        self.address = address


    '''Collect all of urls that we want to crawl data'''

    def get_url(self, year_start, year_end, month_start, month_end, day_start, day_end):
        # url_address = 'san-francisco'
        url_address = self.address
        url_head = 'https://www.timeanddate.com/scripts/cityajax.php?n=usa/'
        url_mid = '&mode=historic&hd='
        url_mid_two = '&month='
        url_tail = '&year='

        '''A method save variable we need with for loop'''
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
        '''Second method save variable we need with for loop
           It\'s so abnormal, even thought it\'s convenience but it\'s so hard to read'''
        # url_pool = [(url_head + url_address + url_mid + str(year) + str(('%02d' % month).zfill(2)) +
        #             str(('%02d' % day).zfill(2)) + url_mid_two + str(month) + url_tail + str(year))
        #             for year in range(year_start, year_end) for month in range(month_start, month_end)
        #             for day in range(day_start, day_end)]
        # date_list = [(str(year) + str(('%02d' % month).zfill(2)) + str(('%02d' % day).zfill(2)))
        #              for year in range(year_start, year_end) for month in range(month_start, month_end)
        #              for day in range(day_start, day_end)]
        return url_pool, date_list


'''Wrap up all the functions (get url, get date list and create file to save data) of first method
   to be a class so that we can let other class inherit this class'''


class PrepositiveMeasureVerOne(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerOne, self).__init__(save_path=save_path, year_initial=year_initial,
                                                          year_conclude=year_conclude, address=address)

    '''This method is applicable to crawl data in a year'''

    def get_job_date(self, name):
        '''A method to get url let every worker to do something they should to do'''
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
        '''Second method'''
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
        # file = self.path + str(year_begin) + '/thread-test-weather-' + str(worker[-3:]) + '.csv'
        file = self.path + str(self.year_initial) + '/weather-' + str(int(int(worker[-3:]) % 12) + 1) + '.csv'
        csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
        write_file = csv.writer(csv_file)
        return csv_file, write_file


'''Wrap up all the functions (get url, get date list and create file to save data) of second method
   to be a class so that we can let other class inherit this class'''


class PrepositiveMeasureVerTwo(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerTwo, self).__init__(save_path=save_path, year_initial=year_initial,
                                                          year_conclude=year_conclude, address=address)

    '''Third method, we want to get ten years data in one time.'''

    def get_job_date(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 12)
            # if int(worker[-3:]) >= 12*mul and int(worker[-3:]) < 12*(mul+1):
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

    '''This function aim to get ten years data in one time'''

    def open_file(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 12)
            # if int(worker[-3:]) >= 12*mul and int(worker[-3:]) < 12*(mul+1):
            year = self.year_initial + 1 * mul
            file = self.path + str(year) + '/weather-' + str(int(int(worker[-3:]) % 12) + 1) + '-month.csv'
            # file = self.path + '2013/thread-test-weather-' + str(worker[-3:]) + '.csv'
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


'''Wrap up all the functions (get url, get date list and create file to save data) of third method
   to be a class so that we can let other class inherit this class'''


class PrepositiveMeasureVerThree(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerThree, self).__init__(save_path=save_path, year_initial=year_initial,
                                                            year_conclude=year_conclude, address=address)

    '''Forth method, we want to use more threads to get ten years data in one time.'''

    '''Quesion : is it better? More faster?
       Answer 1 :  we crawl from 2009 to 2011 about 2 years and 1 month, took 16.278 seconds
       Answer 2 : we crawl from 2009 to 2013 about 4 years and 1 month, took 30.092 seconds
       Answer 3 : we crawl from 2013 to 2017 about 4 years, took 36.027 seconds
       we look the time it spend in average time, unfortunately, it is a little slower than the
       situation that we use less threads'''

    def get_job_date(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 24)
            # if int(worker[-3:]) >= 24*mul and int(worker[-3:]) < 24*(mul+1):
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

    '''This function aim to more faster to get ten years data in one time'''

    def open_file(self, worker):
        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 24)
            if int(worker[-3:]) >= 24 * mul and int(worker[-3:]) < 24 * (mul + 1):
                year = self.year_initial + 1 * mul
                # file = self.path + '2013/thread-test-weather-' + str(worker[-3:]) + '.csv'
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


'''This class inherit the class Get_Condition, so we can use the objects or functions in Get_Condition'''


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
                        # time = row.select('th')[0].text
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
                        # time.sleep(random.random())
                        # time.sleep(random.randint(random(1, 4)+random(2, 3), random(4, 13)+random(4, 7)))
                    index += 1
                    print('第' + str(index) + '天資料記錄成功 ! - ' + str(worker))


    @threads(120)
    def main_job(self, worker):
        crawl_start_time = time.time()
        fields = ['Date', 'Time', 'Temperature', 'Weather', 'Wind', 'Wind Direction', 'Humidity', 'Barometer', 'Visibility']
        csv_file, write_file = self.open_file(worker)
        write_file.writerow(fields)
        url_pool, date_list = self.get_job_date(worker)
        self.parser(url_pool, date_list, write_file, worker)
        csv_file.close()
        crawl_end_time = time.time()
        print('------------------------')
        print('Total time: ' + str(crawl_end_time - crawl_start_time) + ' seconds.')
        print('Crawler Finish.')
        print('------------------------')


if __name__ == '__main__':
    print('Program start.')

    threads_num = 120
    year_start = 2009
    year_end = 2010
    crawl_address = 'san-jose'
    path = 'D:/DataSource/Python/test/bdse08-02-weather-data/weather-' + crawl_address + '-true-fin-module-bsthreads/' + crawl_address + '-weather-'

    '''Check the path is exit or not, if not, then build it.'''
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
