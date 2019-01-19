from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import requests
import sqlite3
import random
import time
import csv



class Parameter:
    def __init__(self, url, head_url):
        self.url = url
        self.head_url = head_url
    

class Sql_DataBase:
    def connect_database(self):
        connect_sql = sqlite3.connect('multiple_conn_ver_2.sqlite')
        job_content_sql = connect_sql.cursor()
        return connect_sql, job_content_sql


    def create_table(self, connect_sql, job_content_sql):
        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS job_opening ("job_name" TEXT NOT NULL, "average_price" INTEGER, \
                         "skills" TEXT, "job_link" varchar(255) PRIMARY KEY NOT NULL)'
        job_content_sql.execute(sql_create_cmd)
        connect_sql.commit()
        print('Table in database job_opening has been created success !')


    def insert_data(self, job_content_sql, data_list):
        sql_insert_cmd = 'INSERT INTO job_opening ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)'
        job_content_sql.execute(sql_insert_cmd, data_list)


class File:

    '''
    Record the data be lose when program is crawling.
    '''

    def record_lose_data(self):
        lose_data_path = r'C:\Users\iAirJordan\Desktop\lose_data_page.csv'
        lose_data_file = open(lose_data_path, 'a+', encoding='utf-8-sig', newline='')
        csv_lose_file = csv.writer(lose_data_file)
        return lose_data_file, csv_lose_file


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


    '''
    We have to pay attention to this function because we use free proxies from google search, it's unstable, it may cause 
    we some trouble like reduce rate of crawler, even as let the net work be down.
    '''

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
            # print('divide 0')
            return divide_num
        else:
            # print('divide 1')
            new_divide_num = divide_num + 1
            return new_divide_num


    def get_url(self, url):
        html = requests.get(url, headers=self.get_header())
        return html


    def crawl(self, html, head_url, page, miss_list, lock, thread_sql, thread_job_sql, worker):

        file_object = File()

        if html.status_code == requests.codes.ok:
            soup = BeautifulSoup(html.text, 'html.parser')
            data_rows = soup.select('a.JobSearchCard-primary-heading-link')
            all_avg_price = soup.select('div.JobSearchCard-secondary-price')
            job_name_list = [data_row.text.strip() for data_row in data_rows]
            avg_price_list = [avg_price.text.strip()[:20].strip() if 'Avg' or 'Bid' in avg_price.text else avg_price.text.strip()
                              for avg_price in all_avg_price] if all_avg_price else ''
            skills_list = [self.crawl_get_job_skill(head_url + (data_row.get('href'))) for data_row in data_rows]
            job_url_list = [(head_url + (data_row.get('href'))) for data_row in data_rows]

            if len(job_name_list) == len(job_url_list):
                if len(job_name_list) == 0:
                    pass
                    # print('Page ' + str(page) + ', has no data. - ' + str(worker))
                else:

                    '''
                    Start to insert data to SQLite DataBase, so execute thread lock to lock the process to ensure here 
                    only has one thread execute prevent for error about SSL happen with multithreading.
                    '''

                    lock.acquire()

                    try:
                        # print('Thread be lock - ' + str(worker))
                        for index in range(0, len(job_name_list)):
                            data_list = [job_name_list[index], avg_price_list[index], skills_list[index], job_url_list[index]]
                            thread_sql.insert_data(thread_job_sql, data_list)
                    except:
                        print('Index has been out of range. - ' + str(worker))
                        pass

                    lock.release()

                    '''
                    It has finished that insert data to DataBase. It is available to release lock to let one of other thread
                    to coming this section to insert data.
                    '''

                    # print('Thread be release - ' + str(worker))
                    print('Page ' + str(page) + ', ' + str(len(job_name_list)) + ' data has been recorded success !!! - ' + str(worker))
            else:
                print('------------------------------------------------')
                # print('The length of job_name_list: ', len(job_name_list))
                # print('The length of skills_list: ', len(skills_list))
                # print('The length of job_url_list: ', len(job_url_list))
                # print('Each of length of these list are different, data is missed.')
                # miss_list.append(int(page))
                lose_data_file, csv_lose_file = file_object.record_lose_data()
                csv_lose_file.writerow(int(page))
                lose_data_file.close()
                print('The page that data is missed has been recorded. - ' + str(worker))
                print('------------------------------------------------')
            return miss_list


    def crawl_get_job_skill(self, target_url):
        target_html = requests.get(target_url, headers=self.get_header())
        if target_html.status_code == requests.codes.ok:
            skill_soup = BeautifulSoup(target_html.text, 'html.parser')
            skill_rows = skill_soup.select('a.PageProjectViewLogout-detail-tags-link--highlight')
            if skill_rows:
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
            else:
                skill_rows_2 = skill_soup.select('ul.logoutHero-recommendedSkills > li')
                if skill_rows_2:
                    i = 1
                    all_skill = ''
                    for skill in skill_rows_2:
                        all_skill = all_skill + str(skill.text) + '、'
                        i += 1
                    new_all_skill_2 = all_skill[:-1]
                else:
                    new_all_skill_2 = ''
                return new_all_skill_2


    def get_time(self, test_url):
        html = self.get_url(test_url)
        if html.status_code == requests.codes.ok:
            soup = BeautifulSoup(html.text, 'html.parser')
            data_rows = soup.select('a.JobSearchCard-primary-heading-link')
            job_name_list = [data_row.text.strip() for data_row in data_rows]
            return len(job_name_list)


class Main_Work(threading.Thread, Parameter, Crawl):

    '''
    Main job what to do in every threads
    '''

    def __init__(self, lock, url, head_url, all_web_page, thread_num):
        threading.Thread.__init__(self)
        # super(Main_Work, self).__init__(url=url, head_url=head_url)
        self.lock = lock
        self.url = url
        self.head_url = head_url
        self.all_web_page = all_web_page
        self.thread_num = thread_num


    def run(self):
        get_data_start = time.time()

        '''
        I think it's important here. We have to know if we want to crawl data and connect SQLite DataBase to let data insert
        in DB, then we have to connect DB in one the same thread and do something we want to do. 
        '''

        print('------Start connect with SQLite DataBase.------')
        thread_sql = Sql_DataBase()
        thread_conn_sql, thread_job_sql = thread_sql.connect_database()

        miss_data_page_list = []
        divide_num = int(int(self.all_web_page) / self.thread_num) + 1
        print('The thread\'s responsible for from page ' + str(int(self.getName()[-3:]) * divide_num) + ' to ' +
              str((int(self.getName()[-3:]) + 1) * divide_num) + '. - ' + str(self.getName()))
        for page in range(int(self.getName()[-3:]) * divide_num, (int(self.getName()[-3:]) + 1) * divide_num):
            aim_url = self.url + str(page)
            html = self.get_url(aim_url)
            miss_data_page_list = self.crawl(html, self.head_url, page, miss_data_page_list, self.lock, thread_sql, thread_job_sql, self.getName())
            thread_conn_sql.commit()

        thread_conn_sql.close()
        print('------Close the connect wih SQLite DataBase.------')
        print('Finish ! ! ! - ' + str(self.getName()))
        print('-----------Get data success ! -----------')
        if miss_data_page_list:
            print('Unfortunately, your data miss something. The page that data is miss below:')
            print(miss_data_page_list)
        else:
            print('Congratulation ! The data is not miss any data !')
        get_data_end = time.time()
        print('-----------Total time : ' + str(get_data_end - get_data_start) + ' seconds. - ' + str(self.getName()) + ' -----------')


if __name__ == '__main__':
    program_start = time.time()

    thread_num = 50

    target_url = 'https://www.freelancer.com/jobs/'
    web_head_url = 'https://www.freelancer.com'
    # save_file_dir = 'C:/Users/iAirJordan/Desktop/jupyter-data/prevent-data-sqldb/'

    sql_db = Sql_DataBase()
    conn_sql, job_sql = sql_db.connect_database()
    sql_db.create_table(conn_sql, job_sql)
    conn_sql.close()

    '''
    We want to get all data in the web, so we need to get all page of the web.
    '''
    get_page_num = Automatic_Web(url=target_url, head_url=web_head_url)
    page_num = get_page_num.driver()

    thread_lock = threading.Lock()

    print('Start to get data we want !')
    thread_list = []
    for k in range(thread_num):
        thread_list.append(Main_Work(lock=thread_lock,
                                     url=target_url,
                                     head_url=web_head_url,
                                     all_web_page=page_num,
                                     thread_num=thread_num))
        thread_list[k].setName('worker-'+str('%003d' % (k-1)))
        thread_list[k].start()

    for k in range(thread_num):
        # print('It join ...... - ' + str(k))
        thread_list[k].join()

    program_end = time.time()
    print('=====Finish all job !!!===== - main_thread')
    print('Total time: ' + str(program_end - program_start) + ' seconds. - main_thread')


'''
Note of program :

Error :
sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.The object was created 
in thread id 44440 and this is thread id 64032

Solution :
SQLite objects (the conneciton, and the cursor) in the same method.

The solution consultation url :
https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
'''