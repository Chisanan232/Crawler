from pyquery import PyQuery as pq
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import random
import time
import csv



class Fake_Identity:
    def get_header(self):
        user_agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                      'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50'
                      ]
        headers = {'User-Agent':random.choice(user_agent)}
        return headers


    # proxies = {'https':''}
    def get_proxy(self):
        proxy = ['5.39.48.34:443',    #super hide
                 '47.52.209.8:80',
                 '110.232.86.52:53281',    #super hide
                 '142.93.11.154:8080',
                 '219.76.152.80:80'     #111 proxies
                 ]
        proxies = {
            'http':'http://' + random.choice(proxy)
            }
        return proxies


class Pq_Crawler:
    fake_id = Fake_Identity()
    fake_user_agent = fake_id.get_header()
    fake_proxy = fake_id.get_proxy()

    def open_file(self):
        # remember change your path
        weather_file = 'D:/DataSource/Python/test/weather-2-class-q.csv'
        file = open(weather_file, 'a+', newline='', encoding='utf-8-sig')
        write_csv_file = csv.writer(file)
        return file, write_csv_file


    def crawl(self, url):
        try:
            # q = pq(url=url, proxies={'http':'219.76.152.80:80'}, headers=get_header())
            q = pq(url=url, proxies=self.fake_proxy, headers=self.fake_user_agent)
        except BaseException as e:
            print('BaseException : ', e)
            print('Let\'s try it again...')
            request_retry = requests.adapters.HTTPAdapter(max_retries=3)
            pq(url, request_retry)
        return q


    def parser(self, q):
        weather = q('tbody').text()
        wind_list = []
        try:
            for index in range(28):
                wind = q('span.comp').eq(index).attr('title')
                wind_list.append(wind)
        except:
            pass
        return weather, wind_list


    def sort_data(self, weather_data, num):
        data = [weather_data]
        data2 = data[0].split(sep='\n')
        # print(data2)
        del data2[1]
        # n = 8
        n = num
        data3 = [data2[i:i + n] for i in range(0, len(data2), n)]
        # print(data3)
        return data3


    def get_data(self, data, wind_list, write_csv_file):
        day = str(year) + m.zfill(2) + d.zfill(2)
        for j in range(0, len(data)):
            data[j].insert(0, day)
            try:
                final_data[j][5] = wind_list[j]
            except:
                pass
            write_csv_file.writerow(data[j])
            print('第' + str(j) + '筆資料記錄成功 !')


if __name__ == '__main__':
    qcrawl = Pq_Crawler()
    file, file_write = qcrawl.open_file()
    fields = ['Date', 'Time', 'Weather', 'Temperature', 'Wind', 'Barometer', 'Wind Direction', 'Humidity', 'Visibility']
    file_write.writerow(fields)

    url_head = 'https://www.timeanddate.com/scripts/cityajax.php?n=usa/new-york&mode=historic&hd='
    url_mid = '&month='
    url_tail = '&year='

    print('start to get data !')
    tStart = time.time()

    for year in range(2013, 2014):
        for month in range(1, 3):
            m = '%02d' % month
            try:
                for day in range(1, 10):
                    d = '%02d' % day
                    target_url = url_head + str(year) + m.zfill(2) + d.zfill(2) + url_mid + str(month) + url_tail + str(
                        year)
                    print(target_url)
                    q = qcrawl.crawl(target_url)
                    weather, wind_data = qcrawl.parser(q)
                    final_data = qcrawl.sort_data(weather, 8)
                    qcrawl.get_data(final_data, wind_data, file_write)
                    # time.sleep(random.randint(random.randint(1, 7), random.randint(8, 13)))
            except BaseException as e:
                print('Error : ', e)
            except:
                print('This month does not have 31 days.')
                pass

    file.close()

    print('finish')
    tEnd = time.time()
    print('this crawler program totally take ' + str(tEnd-tStart) + ' seconds to get data.')


