from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sqlite3
import random
import time



class Parameter:
    def __init__(self, url, head_url):
        self.url = url
        self.head_url = head_url


class Sql_DataBase:
    def create_database(self):
        # You can set your SQLite DataBase name here. (ex: boss.sqlite)
        conn_sql = sqlite3.connect('boss.sqlite')
        job_sql = conn_sql.cursor()
        conn_sql.commit()
        print('Database has been created success !')
        return conn_sql, job_sql


    def create_table(self, job_sql, conn_sql):
        # You can set your table name in SQLite DataBase here. (ex: job_web)
        sqlcmd = 'CREATE TABLE IF NOT EXISTS job_web ("job_name" TEXT NOT NULL, "average_price" TEXT, "skills" TEXT, "job_link" varchar(255))'
        job_sql.execute(sqlcmd)
        conn_sql.commit()
        print('Table in database job_web has been created success !')


    def insert_data(self, conn_sql, job_sql, job_name, new_avg_price, skills, job_url):
        sqlcmd = 'INSERT INTO job_web ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)'
        # sqlcmd_error = 'INSERT INTO ' + self.database_table + ' ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)'
        job_sql.execute(sqlcmd, (job_name, new_avg_price, skills, job_url))
        # job_sql.execute('INSERT INTO job_web ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)', (job_name, new_avg_price, skills, job_url))

        # job_sql.execute('insert into job_web values ("'+str(job_name)+'", "'+str(new_avg_price)+'", "'+str(skills)+'", "'+str(job_url)+'")')
        # job_sql.execute("insert into %s values ('%s', '%s', '%s', '%s')" % ('job_web', job_name, new_avg_price, skills, job_url))
        conn_sql.commit()


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

        '''
        Set the 0.7 seconds here because we have to wait website to execute code I write and get the target number.
        '''

        print('Program will stop 1 seconds.')
        time.sleep(1)
        last_page_url = browser.current_url
        print(last_page_url)
        web_page = int(last_page_url[-4:-1])
        print('We got the last page is ' + str(web_page) + ' ! ! !')
        browser.close()
        browser.quit()
        return web_page


class Crawl(Protect_Measure):
    def get_url(self, target_url):
        html = requests.get(target_url, headers=self.get_header())
        return html


    def crawl(self, html, head_url, job_sql, conn_sql, sql_db, page, miss_list):
        if html.status_code == requests.codes.ok:
            soup = BeautifulSoup(html.text, 'html.parser')
            data_rows = soup.select('a.JobSearchCard-primary-heading-link')
            all_avg_price = soup.select('div.JobSearchCard-secondary-price')
            job_name_list = [data_row.text.strip() for data_row in data_rows]
            avg_price_list = [avg_price.text.strip()[:20].strip() if 'Avg' or 'Bid' in avg_price.text else avg_price.text.strip() for avg_price in all_avg_price] if all_avg_price else ''
            skills_list = [self.crawl_get_job_skill(head_url + (data_row.get('href'))) for data_row in data_rows]
            job_url_list = [(head_url + (data_row.get('href'))) for data_row in data_rows]

            if len(job_name_list) == len(skills_list) == len(job_url_list):
                for index in range(0, len(job_name_list)):
                    sql_db.insert_data(conn_sql, job_sql, job_name_list[index], avg_price_list[index], skills_list[index], job_url_list[index])
            else:
                print('------------------------------------------------')
                # print('The length of job_name_list: ', len(job_name_list))
                # print('The length of skills_list: ', len(skills_list))
                # print('The length of job_url_list: ', len(job_url_list))
                # print('Each of length of these list are different, data is missed.')
                miss_list.append(page)
                print('The page that data is missed has been recorded.')
                print('------------------------------------------------')

            print('Page ' + str(page) + ', ' + str(len(job_name_list)) + ' data has been recorded success !!!')
            return miss_list


    def crawl_get_job_skill(self, target_url):
        target_html = requests.get(target_url)
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


class Main_Work(Parameter, Crawl):
    def __init__(self, url, head_url, all_web_page):
        super(Main_Work, self).__init__(url=url, head_url=head_url)
        self.all_web_page = all_web_page


    def main_job(self, job_sql, conn_sql, sql_db):
        get_data_start = time.time()

        miss_data_page_list = []
        for page in range(1, int(self.all_web_page) + 1):
            aim_url = self.url + str(page)
            html = self.get_url(aim_url)
            miss_data_page_list = self.crawl(html, self.head_url, job_sql, conn_sql, sql_db, page, miss_data_page_list)

        conn_sql.close()
        print('Finish ! ! !')
        print('-----------Get data success ! -----------')
        if miss_data_page_list:
            print('Unfortunately, your data miss something. The page that data is miss below:')
            print(miss_data_page_list)
        else:
            print('Congratulation ! The data is not miss any data !')
        get_data_end = time.time()
        print('-----------Total time : ' + str(get_data_end-get_data_start) + ' seconds. -----------')


if __name__ == '__main__':
    target_url = 'https://www.freelancer.com/jobs/'
    web_head_url = 'https://www.freelancer.com'

    sql_db = Sql_DataBase()
    get_page_num = Automatic_Web(url=target_url, head_url=web_head_url)
    all_page = get_page_num.driver()

    get_data = Main_Work(url=target_url, head_url=web_head_url, all_web_page=all_page)

    conn_sql, job_sql = sql_db.create_database()
    sql_db.create_table(job_sql, conn_sql)

    print('Start to get data we want !')

    get_data.main_job(job_sql, conn_sql, sql_db)
