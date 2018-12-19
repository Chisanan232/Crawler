from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import requests
import random
import time
import csv



class Fake_Identity:
    def get_header(self):
        user_agent = [
            'Here put some available user agent, below are some example from internet.'
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
        proxy = [
            'Here put some available proxy ip, below are some example from internet, now it is unusable I think.'
            '217.61.125.74:3128',
            '118.178.93.238:8888',
            '212.237.15.108:8080',
            '206.189.220.129:8080',
            '114.202.2.185:80',
            '206.189.222.146:8080'
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


class File:
    def open_file(self):
        weatherfile = 'The path where save data we crawled'
        file = open(weatherfile, 'a+', newline='')
        csv_write_file = csv.writer(file)
        return file, csv_write_file


class Bs_Crawler:
    fake_id = Fake_Identity()
    fake_header = fake_id.get_header()
    fake_proxy = fake_id.get_proxy()

    def parser(self, target_url, write_in_file):
        html = requests.get(target_url, headers=self.fake_header, proxies=self.fake_proxy)

        if html.status_code == requests.codes.ok:

            soup = BeautifulSoup(html.text, 'html.parser')

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

                Date = str(year) + m.zfill(2) + d.zfill(2)

                nws = [Date, newTime, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1]
                write_in_file.writerow(nws)

            print('Data has been recorded success !')
            time.sleep(random.randint(random.randint(1, 4)+random.randint(2, 3), random.randint(4, 13)+random.randint(4, 7)))


if __name__ == '__main__':

    crawl = Bs_Crawler()
    build_file = File()

    f, file = build_file.open_file()
    fields = ['Date', 'Time', 'Weather', 'Temperature', 'Wind', 'Barometer', 'Wind Direction', 'Humidity', 'Visibility']
    file.writerow(fields)

    urlhead = 'https://www.timeanddate.com/scripts/cityajax.php?n=usa/san-francisco&mode=historic&hd='
    urlmid = '&month='
    urltail = '&year='

    year_start = 2013    # You can change it to the year you want to crawl.
    year_end = 2014
    month_start = 1      # It's the same with year, you can change it to the month you want.
    month_end = 13
    day_start = 1        # Just change too, if you want.
    day_end = 32

    for year in range(year_start, year_end):
        for month in range(month_start, month_end):
            m = "%02d" % month
            try:
                for date in range(day_start, day_end):
                    d = "%02d" % date
                    url = urlhead + str(year) + m.zfill(2) + d.zfill(2) + urlmid + str(month) + urltail + str(year)
                    print(url)
                    try:
                        crawl.parser(url, file)
                    except BaseException as e:
                        print('BaseException : ', e)
                        print('Let\'s try again...')
                        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
                        requests.get(url, request_retry)
                        continue
            except:
                print('This month does not have 31 days.')

    f.close()
    print('finish')
