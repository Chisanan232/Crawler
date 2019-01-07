from bs4 import BeautifulSoup
import asyncio
import aiohttp
import pandas as pd
import random
import time
import csv
import os


class DefineParameter:
    def __init__(self, save_path, year_initial, year_conclude):
        self.path = save_path
        self.year_initial = year_initial
        self.year_conclude = year_conclude


class ProtectMeasure:
    def get_header(self):
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
        proxies_pool = [
            'http://58.11.72.35:3128',
            'http://77.74.224.37:53081',
            'http://103.24.110.21:39689',
            'http://118.174.65.137:54063',
            'http://203.151.50.213:3128',
            'http://95.87.202.118:80',
            'http://217.196.64.201:50885	',
            'http://104.248.208.209	:8080',
            'http://201.148.167.161	:61547',
            'http://189.206.175.169:50555',
            'http://195.13.201.98:40511',
            'http://191.252.192.46:80',
            'http://72.249.211.149:33075',
            'http://177.21.118.124:20183',
            'http://103.233.121.19:43792',
            'http://190.110.202.230:46061',
            'http://109.160.91.187:23500',
            'http://213.6.225.202:40766',
            'http://83.218.124.155:41258',
            'http://91.143.172.93:30360',
            'http://103.65.193.222:30151',
            'http://121.101.190.246:43708',
            'http://141.105.99.160:40801',
            'http://163.158.214.132	:80'
        ]
        proxy = {
            'http': 'http://' + random.choice(proxies_pool),
            'https': 'https://' + random.choice(proxies_pool)
        }
        return proxy


class File(DefineParameter):
    def __init__(self, save_path, year_initial, year_conclude):
        super(File, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)


    def open_file(self, date):
        if not os.path.exists(self.path + str(date)[:4] + '/'):
            try:
                os.makedirs(self.path + str(date)[:4] + '/')
                print(self.path + str(date)[:4] + '/')
                print('Build folder success !!!')
            except BaseException as e:
                print('Error: ', e)
                print('If this error about file or direction exist so cannot build, then we don\'t care it.')
        else:
            print('File exists already.')
            pass
        file = self.path + str(date)[:4] + '/weather-' + str(date)[4:6] + '-month.csv'
        csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
        write_file = csv.writer(csv_file)
        return csv_file, write_file


class MergeData(DefineParameter):
    def __init__(self, save_path, year_initial, year_conclude, address, save_file_dir, save_path_file_name):
        super(MergeData, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)
        self.address = address
        self.save_file_dir = save_file_dir
        self.save_path_file_name = save_path_file_name


    def merge(self):
        new_path_dir_str = '/'
        path_str_list = self.path.split(sep='/')
        path_str_list.remove(path_str_list[-1])
        new_path_dir = new_path_dir_str.join(path_str_list)
        weather_year = [pd.DataFrame(pd.read_csv(os.path.join(new_path_dir, data_folder, file))) for data_folder in
                        os.listdir(new_path_dir) for file in os.listdir(os.path.join(new_path_dir, data_folder))]
        '''No. 1 method'''
        # new_weather_year = []
        # for weather_data in weather_year:
        #     weather_group = weather_data.groupby('Date')
        #     new_weather = pd.concat([weather_group.get_group(date) for date in sorted(set(weather_data['Date']))], axis=0, ignore_index=True)
        #     new_weather_year.append(new_weather)
        '''No. 2 method'''
        new_weather_year = [pd.concat([weather_data.groupby('Date').get_group(date) for date in
                                       sorted(set(weather_data['Date']))], axis=0, ignore_index=True)
                            for weather_data in weather_year]
        weather_data = pd.concat(new_weather_year, axis=0, ignore_index=True)

        save_path = self.save_file_dir + str(self.address) + self.save_path_file_name
        pd.DataFrame(weather_data).to_csv(save_path, encoding='utf-8-sig', index=False)
        print('------Data has been merged finish !-------')


class All_Url_In_Worker(DefineParameter):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(All_Url_In_Worker, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)
        self.address = address


    def get_url(self, year_start, year_end, month_start, month_end, day_start, day_end):
        url_address = self.address
        url_head = 'https://www.timeanddate.com/scripts/cityajax.php?n=usa/'
        url_mid = '&mode=historic&hd='
        url_mid_two = '&month='
        url_tail = '&year='

        url_pool = [(url_head + url_address + url_mid + str(year) + str(('%02d' % month).zfill(2)) +
                     str(('%02d' % day).zfill(2)) + url_mid_two + str(month) + url_tail + str(year))
                    for year in range(year_start, year_end) for month in range(month_start, month_end)
                    for day in range(day_start, day_end)]
        date_list = [(str(year) + str(('%02d' % month).zfill(2)) + str(('%02d' % day).zfill(2)))
                     for year in range(year_start, year_end) for month in range(month_start, month_end)
                     for day in range(day_start, day_end)]
        return url_pool, date_list


class CrawlerThread(ProtectMeasure, All_Url_In_Worker):
    def __init__(self, save_path, year_initial, year_conclude, address, month_initial, month_conclude):
        super(CrawlerThread, self).__init__(save_path=save_path, year_initial=year_initial,
                                            year_conclude=year_conclude, address=address)
        self.month_initial = month_initial
        self.month_conclude = month_conclude


    async def send_requests(self, session, url):
        try:
            async with session.get(url, headers=self.get_header()) as response:
                assert response.status == 200
                html = await response.read()
                return response.url, html
            # response = await session.get(url)
            # return str(response.read())
        except:
            pass


    def parse(self, html, target_url, date_list):
        build_file = File(save_path=self.path, year_initial=year_start, year_conclude=year_end)

        for date in date_list:
            if date in str(target_url):
                soup = BeautifulSoup(html, 'html.parser')
                web_data = soup.select('tbody > tr')[0].text
                if web_data == 'No data available for the given date. Try selecting a different day.':
                    print('--------------------------')
                    print('There isn\'t have any data here')
                    print('--------------------------')
                    date_list.remove(date)
                else:
                    if not os.path.exists(self.path + str(date)[:4] + '/weather-' + str(date)[4:6] + '-month.csv'):
                        fields = ('Date', 'Time', 'Weather', 'Temperature', 'Wind', 'Barometer', 'Wind Direction',
                                   'Humidity', 'Visibility')
                        csv_file, write_file = build_file.open_file(date)
                        write_file.writerow(fields)
                    else:
                        csv_file, write_file = build_file.open_file(date)
                        dataRow = soup.select('tbody > tr')
                        for row in dataRow:
                            Time = row.select_one('th').text
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

                            datalist = [newTime, weather, Temp1, wind, Barometer, wind_dir, Humidity, Visibility1]
                            datalist.insert(0, date)
                            write_file.writerow(datalist)
                        if int(date[-2:]) == 1:
                            print('The data of ' + str(date)[-2:] + 'st day has been recorded success !')
                        elif int(date[-2:]) == 2:
                            print('The data of ' + str(date)[-2:] + 'nd day has been recorded success !')
                        elif int(date[-2:]) == 3:
                            print('The data of ' + str(date)[-2:] + 'rd day has been recorded success !')
                        else:
                            print('The data of ' + str(date)[-2:] + 'th day has been recorded success !')


    async def get_results(self, session, url, date_list):
        url, html = await self.send_requests(session, url)
        self.parse(html, url, date_list)


    async def main(self, loop):
        async_start = time.time()

        async with aiohttp.ClientSession() as session:
            urls_pool, date_list = self.get_url(self.year_initial, self.year_conclude, self.month_initial,
                                                self.month_conclude, 1, 32)
            tasks = [loop.create_task(self.get_results(session, url, date_list)) for url in urls_pool]
            finished, unfinished = await asyncio.wait(tasks)
            all_results = [r.result() for r in finished]
            print(all_results)
            print('\n')

        async_end = time.time()
        print('========================')
        print('Total: ' + str(async_end - async_start) + ' seconds.')
        print('Program Finish.')


if __name__ == '__main__':
    crawl_address = 'mountain-view'      # The address where you want to crawl to get weather data.
    year_start = 2014                    # The year you want to get data
    year_end = 2015
    month_start = 1                      # The month you want to get data
    month_end = 13

    path = 'The path where save data you crawled'
    path_dir = 'The path where save file that merge all data you crawled'
    path_file_name = 'The file name that save file merge all data you crawled'

    asyncio_crawler = CrawlerThread(save_path=path,
                                    year_initial=year_start,
                                    year_conclude=year_end,
                                    address=crawl_address,
                                    month_initial=month_start,
                                    month_conclude=month_end)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio_crawler.main(loop))

    merge_data = MergeData(save_path=path,
                           year_initial=year_start,
                           year_conclude=year_end,
                           address=crawl_address,
                           save_file_dir=path_dir,
                           save_path_file_name=path_file_name)
    merge_data.merge()

    print('=========== Program Finish ! =========')


'''Note about this program'''
'''First time, try to crawled data of 1 year, it took 24.53438639640808 seconds'''