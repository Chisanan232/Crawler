from bs4 import BeautifulSoup
import requests
import random
import time
import csv


# Setting headers to hide the identity that we are crawler program, it can avoid block by web server.
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

# Our data's headers
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

        # Download content of the web and get the source code of the web
        html = requests.get(url, headers=get_header())

        # Make sure we download success or not
        if html.status_code == requests.codes.ok:

            # Parse HTML code with BeautifulSoup
            soup = BeautifulSoup(html.text, 'html.parser')

            # Get the data we want by CSS syntax
            tableRow = soup.select('#wt-his > tbody > tr')
            #print(tableRow)

            for row in tableRow:

                Time = row.select_one('th').text
                #time = row.select('th')[0].text

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
                # print('Humidity : ', Humidity)

                Bar = row.select('.sep')[1]
                Visibility = Bar.find_next_siblings('td')[0].text
                # print('Visibility : ', Visibility)

                # print('========================================')

                # We may get some impurity we don't need in data, so we have to remove it.
                Temp1 = "".join(Temp.split())
                Visibility1 = "".join(Visibility.split())
                # nws = [time, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1]
                # print(nws)

                file.writerow([Time, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1])

        # Feign we are human to browse the web to avoid be blocked by web server, and in other hand, decrease stress on
        # server, we are good crawler program.
        time.sleep(random.randint(5, 12))

# Remember close the file you opened, release your memory space, it's easily to forget.
f.close()

print('finish')

