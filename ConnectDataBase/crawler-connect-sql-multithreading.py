'''
I write this program because I want to crawler and insert data to DataBase with multithreading. But there is a question:
Currently, we know the method to realize the idea is to write with python package "threading", but now, I use package is
"tomorrow", it doesn't have "lock" and "release" function to ensure your all threads can crawl data and CONNECT SQL DB
WITHOUT ERROR. In other word, the package "tomorrow" does not have function to ensure in the same time segment we just
only have one thread connect DB and do something like insert data into it. Now I just try to use my algorithm to realize
crawl data and connect DB with multithreading.
'''

from selenium import webdriver
from bs4 import BeautifulSoup
from tomorrow import threads
import pandas as pd
import requests
import sqlite3
import random
import time
import csv
import os



class Parameter:
    def __init__(self, url, head_url):
        self.url = url
        self.head_url = head_url
    

class Sql_DataBase:
    def create_database(self):
        connect_sql = sqlite3.connect('boss-thread.sqlite')
        job_content_sql = connect_sql.cursor()
        return connect_sql, job_content_sql


    def create_table(self, connect_sql, job_content_sql):
        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS job_web ("job_name" TEXT NOT NULL, "average_price" INTEGER, \
                         "skills" TEXT, "job_link" varchar(255) PRIMARY KEY NOT NULL)'
        job_content_sql.execute(sql_create_cmd)
        connect_sql.commit()
        print('Table in database job_web has been created success !')


    def insert_data(self, job_content_sql, data_list):
        sql_insert_cmd = 'INSERT INTO job_web ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)'
        job_content_sql.execute(sql_insert_cmd, data_list)


class File:

    '''
    Distribute all data into a mount of threads number and build the same quantity files where save the data we crawled
    '''

    def create_file(self, worker, target_file_dir):
        fields = ["job_name", "average_price", "skills", "job_link"]
        if target_file_dir[-1] == '/':
            data_file = target_file_dir + 'job-data-thread-' + worker[-3:] + '.csv'
            file = open(data_file, '+a', encoding='utf-8-sig', newline='')
            writer_file = csv.writer(file)
            writer_file.writerow(fields)
            print('Build file success !!! - ' + str(worker))
        else:
            data_file = target_file_dir + '/job-data-thread-' + worker[-3:] + '.csv'
            file = open(data_file, '+a', encoding='utf-8-sig', newline='')
            writer_file = csv.writer(file)
            writer_file.writerow(fields)
            print('Build file success !!! - ' + str(worker))
        return file, writer_file


    def data_merge(self, target_file_dir):
        all_data = pd.concat([pd.DataFrame(pd.read_csv(os.path.join(target_file_dir, file))) for file in
                              os.listdir(target_file_dir)], axis=0, ignore_index=True)
        return all_data


class DataNotReadyError(Exception):

    '''
    Define the exception because after we crawled finish, we will merge all data we crawled and insert it into SQL DB
    '''

    def __init__(self, ErrorInfro):
        super(DataNotReadyError, self).__init__()
        self.errorinfro = ErrorInfro


    def __str__(self):
        return self.errorinfro


class Protect_Measure:
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


    '''We have to pay attention to this function because we use free proxies from google search, it's unstable, it
       may cause we some trouble like reduce rate of crawler, even as let the net work be down.'''
    def get_proxy(self):
        proxies_pool = [
            'http://104.248.208.209	:8080',
            'http://189.206.175.169:50555',
            'http://177.21.118.124:20183',
            'http://103.233.121.19:43792',
            'http://121.101.190.246:43708',
            'http://141.105.99.160:40801',
        ]
        proxy = {
            'http': 'http://' + random.choice(proxies_pool),
            'https': 'https://' + random.choice(proxies_pool)
        }
        return proxy


class Automatic_Web(Parameter, Protect_Measure):

    '''
    We want to get all data of web, so we have to know number of the last page
    '''

    def __init__(self, url, head_url):
        super(Automatic_Web, self).__init__(url=url, head_url=head_url)


    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent=%s' % self.get_header())
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(self.url)
        browser.find_elements_by_css_selector('li.Pagination-item')[6].click()
        print('Program will stop 0.7 seconds.')
        time.sleep(0.7)
        last_page_url = browser.current_url
        print(last_page_url)
        web_page = int(last_page_url[-4:-1])
        print('We got the last page is ' + str(web_page) + ' !')
        browser.close()
        browser.quit()
        return web_page


class Crawl(Protect_Measure):

    '''
    Distribute work (which pages are crawled) thread should be to do to every treads
    '''

    def distribute_url_page(self, page_number, thread_number):
        divide_num = int(int(page_number) / int(thread_number))
        if int(page_number) % int(thread_number) == 0:
            print('divide 0')
            return divide_num
        else:
            print('divide 1')
            new_divide_num = divide_num + 1
            return new_divide_num


    def get_url(self, url):
        html = requests.get(url, headers=self.get_header())
        return html


    def crawl(self, html, head_url, writer_file, page, miss_list, worker):
        if html.status_code == requests.codes.ok:
            soup = BeautifulSoup(html.text, 'html.parser')
            data_rows = soup.select('a.JobSearchCard-primary-heading-link')
            all_avg_price = soup.select('div.JobSearchCard-secondary-price')
            job_name_list = [data_row.text.strip() for data_row in data_rows]
            avg_price_list = [avg_price.text.strip()[:20].strip() if 'Avg' or 'Bid' in avg_price.text else avg_price.text.strip()
                              for avg_price in all_avg_price] if all_avg_price else ''
            skills_list = [self.crawl_get_job_skill(head_url + (data_row.get('href'))) for data_row in data_rows]
            job_url_list = [(head_url + (data_row.get('href'))) for data_row in data_rows]

            if len(job_name_list) == len(skills_list) == len(job_url_list):
                if len(job_name_list) == 0:
                    print('Page ' + str(page) + ', has no data. - ' + str(worker))
                else:
                    for index in range(0, len(job_name_list)):
                        data_list = [job_name_list[index], avg_price_list[index], skills_list[index], job_url_list[index]]
                        writer_file.writerow(data_list)
                    print('Page ' + str(page) + ', ' + str(len(job_name_list)) + ' data has been recorded success !!! - ' + str(worker))
            else:
                print('------------------------------------------------')
                print('The length of job_name_list: ', len(job_name_list))
                print('The length of skills_list: ', len(skills_list))
                print('The length of job_url_list: ', len(job_url_list))
                print('Each of length of these list are different, data is missed.')
                miss_list.append(int(page))
                print('The page that data is missed has been recorded. - ' + str(worker))
                print('------------------------------------------------')
            return miss_list


    def crawl_get_job_skill(self, target_url):
        target_html = requests.get(target_url, headers=self.get_header())
        if target_html.status_code == requests.codes.ok:
            skill_soup = BeautifulSoup(target_html.text, 'html.parser')
            skill_rows = skill_soup.select('a.PageProjectViewLogout-detail-tags-link--highlight')
            if skill_rows:
                i = 1
                all_skill = ''
                for skill in skill_rows:
                    all_skill = all_skill + str(skill.text) + '、'
                    i += 1
                new_all_skill = all_skill[:-1]
            else:
                new_all_skill = ''
            return new_all_skill


    def get_time(self, test_url):
        html = self.get_url(test_url)
        if html.status_code == requests.codes.ok:
            soup = BeautifulSoup(html.text, 'html.parser')
            data_rows = soup.select('a.JobSearchCard-primary-heading-link')
            job_name_list = [data_row.text.strip() for data_row in data_rows]
            return len(job_name_list)



class Main_Work(Parameter, Crawl):

    '''
    Main job what to do in every threads
    '''

    def __init__(self, url, head_url, all_web_page, target_file_dir):
        super(Main_Work, self).__init__(url=url, head_url=head_url)
        self.all_web_page = all_web_page
        self.target_file_dir = target_file_dir


    @threads(50)
    def main_job(self, worker, thread_num):
        get_data_start = time.time()

        # save_file = File()
        file, writer_file = save_file.create_file(worker, self.target_file_dir)

        miss_data_page_list = []
        divide_num = int(int(self.all_web_page) / thread_num) + 1
        print('The thread\'s responsible for from page ' + str(int(worker[-3:]) * divide_num) + ' to ' +
              str((int(worker[-3:]) + 1) * divide_num) + '. - ' + str(worker))
        for page in range(int(worker[-3:]) * divide_num, (int(worker[-3:]) + 1) * divide_num):
            aim_url = self.url + str(page)
            html = self.get_url(aim_url)
            miss_data_page_list = self.crawl(html, self.head_url, writer_file, page, miss_data_page_list, worker)

        print('Finish ! ! ! - ' + str(worker))
        print('-----------Get data success ! -----------')
        if miss_data_page_list:
            print('Unfortunately, your data miss something. The page that data is miss below:')
            print(miss_data_page_list)
        else:
            print('Congratulation ! The data is not miss any data !')
        get_data_end = time.time()
        print('-----------Total time : ' + str(get_data_end - get_data_start) + ' seconds. - ' + str(worker) + ' -----------')


if __name__ == '__main__':
    program_start = time.time()

    thread_num = 50

    target_url = 'https://www.freelancer.com/jobs/'
    web_head_url = 'https://www.freelancer.com'
    save_file_dir = 'D:/DataSource/Python/test/prevent-data-sqldb/'

    sql_db = Sql_DataBase()
    conn_sql, job_sql = sql_db.create_database()
    sql_db.create_table(conn_sql, job_sql)

    get_page_num = Automatic_Web(url=target_url, head_url=web_head_url)
    page_num = get_page_num.driver()

    save_file = File()

    thread_job = Main_Work(url=target_url, head_url=web_head_url, all_web_page=page_num, target_file_dir=save_file_dir)
    print('Start to get data we want !')
    workers_list = ['worker-' + str(('%003d' % i).zfill(3)) for i in range(thread_num)]
    for j in workers_list:
        thread_job.main_job(j, thread_num)

    '''
    After crawled, we will merge all data into a file, and then insert it into DB. In exactly, this step and lines 272 
    step are synchronal, therefore we use the logic from lines 278 to lines 306 and with we define exception ourself to 
    reach that we can be sure all data have been finish, then program will continue.
    '''

    crawler = Crawl()
    data_quantity = crawler.get_time(target_url)
    thread_page = int(page_num / thread_num) + 1
    all_thread_num = int(page_num / thread_page) + 1
    surplus_thread_num = all_thread_num - thread_num
    last_thread_page = page_num - (all_thread_num - 1) * thread_page
    while True:
        try:
            for file in os.listdir(save_file_dir)[:surplus_thread_num]:
                if file == 'job-data-thread-' + str(('%003d' % (thread_num - 1)).zfill(3)) + '.csv':
                    if os.path.getsize(os.path.join(save_file_dir, file)) / 1024 > 0.16 * float(int(data_quantity) *
                                                                                                last_thread_page):
                        print('All data has been recorded success ! Time to insert data to SQL DB ! - main_thread')
                    else:
                        print('Program will sleep for 300 seconds ...... zzzzzzz - main_thread')
                        time.sleep(300)
                        raise DataNotReadyError('Data is not ready ...... - main_thread')
                else:
                    if os.path.getsize(os.path.join(save_file_dir, file)) / 1024 > 0.16 * float(int(data_quantity) *
                                                                                                (int(page_num / thread_num) + 1)):
                        print('All data has been recorded success ! Time to insert data to SQL DB ! - main_thread')
                    else:
                        print('Program will sleep for 300 seconds ...... zzzzzzz - main_thread')
                        time.sleep(300)
                        raise DataNotReadyError('Data is not ready ...... - main_thread')
        except BaseException as e:
            print(e)
            continue
        break
    print('Start to insert data to SQL database. - main_thread')
    data = save_file.data_merge(save_file_dir)
    data_pd = pd.DataFrame(data)
    for index in range(data_pd.count()):
        sql_db.insert_data(job_sql, data_pd.iloc[index])

    program_end = time.time()
    print('=====Finish all job !!!===== - main_thread')
    print('Total time: ' + str(program_end - program_start) + ' seconds. - main_thread')
