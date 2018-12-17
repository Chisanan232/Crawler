from bs4 import BeautifulSoup
import requests
import random
import time
import csv


def get_header():
    user_agent = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Opera/8.0 (Windows NT 5.1; U; en)'
    ]
    headers = {'User-Agent':random.choice(user_agent)}
    return headers


weatherfile = 'The path where save data you crawled'

fields = ['Time', 'Weather', 'Temperature', 'Wind', 'Barometer', 'Wind Direction', 'Humidity', 'Visibility']

f = open(weatherfile, 'a+', newline='')
file = csv.writer(f)
file.writerow(fields)


for year in range(2013, 2014):

    for month in range(1, 13):


        urlhead = 'https://www.timeanddate.com/weather/usa/new-york/historic?month='
        urlmid = '&year='
        url = urlhead + str(month) + urlmid + str(year)

        print(url)

        # 下載這個網頁的內容  # 抓取這個網頁的原始碼
        html = requests.get(url, headers=get_header())

        # 確認是否下載成功
        if html.status_code == requests.codes.ok:

            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(html.text, 'html.parser')

            # 以 CSS 的 class 抓出我們所需要的資料
            tableRow = soup.select('#wt-his > tbody > tr')
            #print(table)
            for row in tableRow:

                Time = row.select_one('th').text
                #time = row.select('th')[0].text

                # 天氣狀況時間
                #    print('Time : ', Time)
                #hit = th[0].text
                # print(Time)

                weather = row.select('.mtt')[0].get('title')
                # print('Weather : ', weather)

                Temp = row.select_one('.wt-ic + td').text
                # print('Temperature : ', Temp)

                wind = row.select('.sep')[0].text
                # print('Wind : ', wind)
                Barometer = row.select('.sep')[1].text
                # print('Barometer : ', Barometer)

                wind_dir = row.select('.comp')[0].get('title')
                #    print('Wind Direction : ', wind_dir)

                Bar = row.select('.sep')[1]
                Humidity = Bar.find_previous_siblings('td')[0].text
                #    print('Humidity : ', Humidity)

                Bar = row.select('.sep')[1]
                Visibility = Bar.find_next_siblings('td')[0].text
                #    print('Visibility : ', Visibility)

                #    print('========================================')

                Temp1 = "".join(Temp.split())
                Visibility1 = "".join(Visibility.split())
                # nws = [time, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1]
                # print(nws)

                # f = open(weatherfile, 'a+', newline='')
                # file = csv.writer(f)
                # file.writerow(fields)
                file.writerow([Time, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1])

        # time.sleep(random.random())
        time.sleep(random.randint(5, 12))



f.close()

print('finish')

