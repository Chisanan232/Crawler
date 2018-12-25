from pyquery import PyQuery as pq
import threading
import pandas as pd
import random
import time
import csv
import sys
import os



class Parameter:
    def __init__(self, save_path, year_initial, year_conclude):
        self.save_path = save_path
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
        ]
        proxy = {
            'http': 'http://' + random.choice(proxies_pool),
            'https': 'https://' + random.choice(proxies_pool)
        }
        return proxy


class AllUrlInWorker(Parameter):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(AllUrlInWorker, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)
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


class MergeData(Parameter):
    def __init__(self, save_path, year_initial, year_conclude, address, save_path_dir, save_path_file_name):
        super(MergeData, self).__init__(save_path=save_path, year_initial=year_initial, year_conclude=year_conclude)
        self.address = address
        self.save_path_dir = save_path_dir
        self.save_path_file_name = save_path_file_name


    def merge(self):
        '''Check the path is exit or not, if not, then build it.'''
        folder = os.path.exists(self.save_path_dir)
        if not folder:
            os.makedirs(self.save_path_dir)
            print(self.save_path_dir)
            print('Build folder success !!!')
        else:
            print('Folder exists.')
            pass

        new_path_dir_str = '/'
        path_str_list = self.save_path.split(sep='/')
        path_str_list.remove(path_str_list[-1])
        new_path_dir = new_path_dir_str.join(path_str_list)

        weather_year = [pd.DataFrame(pd.read_csv(os.path.join(new_path_dir, data_folder, file))) for data_folder in
                        os.listdir(new_path_dir) for file in os.listdir(os.path.join(new_path_dir, data_folder))]
        weather_data = pd.concat(weather_year, axis=0, ignore_index=True)

        save_path = self.save_path_dir + str(self.address) + self.save_path_file_name
        pd.DataFrame(weather_data).to_csv(save_path, encoding='utf-8-sig', index=False)
        print('------Data has been merged finish !-------')


class DataNotReadyError(Exception):
    def __init__(self, ErrorInFor):
        super(DataNotReadyError, self).__init__()
        self.errorinfor = ErrorInFor


    def __str__(self):
        return self.errorinfor


class PrepositiveMeasureVerTwo(AllUrlInWorker):
    def __init__(self, save_path, year_initial, year_conclude, address):
        super(PrepositiveMeasureVerTwo, self).__init__(save_path=save_path, year_initial=year_initial,
                                                       year_conclude=year_conclude, address=address)


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


    def open_file(self, worker, num_thread):
        '''Check the path is exit or not, if not, then build it.'''
        for year in range(self.year_initial, self.year_initial + int(num_thread / 12)):
            folder = os.path.exists(self.save_path + str(year) + '/')
            if not folder:
                try:
                    os.makedirs(self.save_path + str(year) + '/')
                    print(self.save_path + str(year) + '/')
                    print('Build folder success !!!')
                except BaseException as e:
                    print('Error: ', e)
                    print('If this error about file or direction exist so cannot build, then we don\'t care it.')
            else:
                break

        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 12)
            year = self.year_initial + 1 * mul
            file = self.save_path + str(year) + '/weather-' + str(int(int(worker[-3:]) % 12) + 1) + '-month.csv'
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
        super(PrepositiveMeasureVerThree, self).__init__(save_path=save_path, year_initial=year_initial,
                                                         year_conclude=year_conclude, address=address)


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


    def open_file(self, worker, num_thread):
        '''Check the path is exit or not, if not, then build it.'''
        for year in range(self.year_initial, self.year_initial + int(num_thread / 12)):
            folder = os.path.exists(self.save_path + str(year) + '/')
            if not folder:
                try:
                    os.makedirs(self.save_path + str(year) + '/')
                    print(self.save_path + str(year) + '/')
                    print('Build folder success !!!')
                except BaseException as e:
                    print('Error: ', e)
                    print('If this error about file or direction exist so cannot build, then we don\'t care it.')
            else:
                break

        if worker[-3:].isdigit():
            mul = int(int(worker[-3:]) / 24)
            year = self.year_initial + 1 * mul
            if int(int(worker[-3:]) % 24) < 12:
                file = self.save_path + str(year) + '/weather-' + str(
                    int(int(worker[-3:]) % 24) + 1) + '-month-first-two-weeks.csv'
                csv_file = open(file, 'a+', newline='', encoding='utf-8-sig')
                write_file = csv.writer(csv_file)
                return csv_file, write_file
            else:
                file = self.save_path + str(year) + '/weather-' + str(
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


class CrawlerThread(threading.Thread, ProtectMeasure, PrepositiveMeasureVerTwo):
    def __init__(self, number_thread, save_path, year_initial, year_conclude, address):
        threading.Thread.__init__(self)
        # super(CrawlerThread, self).__init__(save_path=save_path, year_initial=year_initial,
        #                                     year_conclude=year_conclude, address=address)
        self.number_thread = number_thread
        self.save_path = save_path
        self.year_initial = year_initial
        self.year_conclude = year_conclude
        self.address = address


    def sort_data(self, weather_data, num):
        data = [weather_data]
        data2 = data[0].split(sep='\n')
        del data2[1]
        # # n = 8
        n = num
        data3 = [data2[i:i + n] for i in range(0, len(data2), n)]
        # # print(data3)
        return data3


    def determine_and_crawl(self, target_url, date_list, write_file, worker):
        count = 0
        data_count = 1
        for url in target_url:
            try:
                # q = pq(url=url)
                q = pq(url=url, headers=self.get_header())
                weather = q('tbody').text()
                if weather == 'No data available for the given date. Try selecting a different day.':
                    print('--------------------------------')
                    print('There is nothing in this date.')
                    print('--------------------------------')
                    for str_date in date_list:
                        if str_date in url:
                            date_list.remove(str_date)
                    pass
                else:
                    wind_list = []
                    try:
                        for index in range(28):
                            wind = q('span.comp').eq(index).attr('title')
                            wind_list.append(wind)
                    except:
                        pass
                    final_data = self.sort_data(weather, 8)
                    for j in range(0, len(final_data)):
                        final_data[j].insert(0, date_list[count])
                        try:
                            final_data[j][5] = wind_list[j]
                            # final_data[j][4] = wind_list[j]
                        except:
                            pass
                        write_file.writerow(final_data[j])
                        # print(final_data[j])
                        # print(date_list[0])
                        # print('The data of ' + str(j) + 'st day has been recorded success ! - ' + str(worker))
                    count += 1
                    if date_list == 1:
                        print('The data of ' + str(data_count) + 'st day has been recorded success ! - ' + str(worker))
                    elif date_list == 2:
                        print('The data of ' + str(data_count) + 'nd day has been recorded success ! - ' + str(worker))
                    elif date_list == 3:
                        print('The data of ' + str(data_count) + 'rd day has been recorded success ! - ' + str(worker))
                    else:
                        print('The data of ' + str(data_count) + 'th day has been recorded success ! - ' + str(worker))
                    # if date_list == 1:
                    #     print('The data in half of ' + str(data_count) + 'st day has been recorded success ! - ' + str(worker))
                    # elif date_list == 2:
                    #     print('The data in half of ' + str(data_count) + 'nd day has been recorded success ! - ' + str(worker))
                    # elif date_list == 3:
                    #     print('The data in half of ' + str(data_count) + 'rd day has been recorded success ! - ' + str(worker))
                    # else:
                    #     print('The data in half of ' + str(data_count) + 'th day has been recorded success ! - ' + str(worker))
                    data_count += 1
            except Exception as e:
                print('-------------------------------------------')
                print('This month only have 30 days.(It\'s has 28 or 29 days if it\'s February.)')
                print('Or it may have other problem?')
                print('-------------------------------------------')
                print(e)
                pass
        print('-----------------------------------------')
        print(str(worker) + ' done the job')
        print('-----------------------------------------')


    def run(self):
        tStart = time.time()

        fields = [tuple(x) for x in
                  ['Date', 'Time', 'Weather', 'Temperature', 'Wind', 'Barometer', 'Wind Direction', 'Humidity',
                   'Visibility']]
        csv_file, write_file = self.open_file(self.getName(), self.number_thread)
        write_file.writerow(fields)
        url_pool, date_list = self.get_job_date(self.getName())
        self.determine_and_crawl(url_pool, date_list, write_file, self.getName())
        csv_file.close()

        tEnd = time.time()
        print('-------------------------------------')
        print('Total time : ' + str(tEnd-tStart) + ' seconds.')
        print('Finish.')
        print('-------------------------------------')


if __name__ == '__main__':
    print('start')

    crawl_address = 'mountain-view'      # The address where you want to crawl to get weather data.
    year_start = 2009                    # The year you want to get data
    year_end = 2010
    num_thread = 120                     # The number of threads

    path = 'The path where save data you crawled'
    path_dir = 'The path where save file that merge all data you crawled'
    path_file_name = 'The file name that save file merge all data you crawled'

    threads_list = []
    for k in range(num_thread):
        threads_list.append(CrawlerThread(save_path=path,
                                          year_initial=year_start,
                                          year_conclude=year_end,
                                          address=crawl_address,
                                          number_thread=num_thread))
        threads_list[k].setName('worker-' + str('%003d' % (k - 1)))
        threads_list[k].start()

    for k in range(num_thread):
        print('It join ...... - ' + str(k))
        threads_list[k].join()

    print('It\'s time to merge all data to a file.')
    merge_method = MergeData(save_path=path,
                             year_initial=year_start,
                             year_conclude=year_end,
                             address=crawl_address,
                             save_path_dir=path_dir,
                             save_path_file_name=path_file_name)
    merge_method.merge()

    print('============program finish !============')


'''note about this program'''
'''first time operate, it just took 72.95139074325562 seconds !'''