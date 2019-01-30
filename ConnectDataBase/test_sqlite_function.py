from bs4 import BeautifulSoup
import requests
import sqlite3


# html = requests.get('https://www.freelancer.com/contest/redesign-a-report-for-stylish-corporate-women-1464476.html')
#
# if html.status_code == requests.codes.ok :
#     soup = BeautifulSoup(html.text, 'html.parser')
#     print(soup)
#     data_rows = soup.select('ul.logoutHero-recommendedSkills > li')
#     for row in data_rows:
#         job_skill = row.text
#         print(job_skill)


def connect_database():
    connect_sql = sqlite3.connect('test_2.sqlite')
    job_content_sql = connect_sql.cursor()
    return connect_sql, job_content_sql


def create_table(table_name, connect_sql, job_content_sql):
    sql_create_cmd = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' ("job_name" TEXT NOT NULL, "average_price" INTEGER, \
                     "skills" TEXT, "job_link" varchar(255) PRIMARY KEY NOT NULL)'
    # sql_create_cmd = 'CREATE TABLE IF NOT EXISTS test_sql_table ("job_name" TEXT NOT NULL, "average_price" INTEGER, \
    #                  "skills" TEXT, "job_link" varchar(255) PRIMARY KEY NOT NULL)'
    print('test')
    job_content_sql.execute(sql_create_cmd)
    connect_sql.commit()
    print('Table in database ' + table_name + ' has been created success !')


def insert_data(table_name, job_content_sql, data_list):
    sql_insert_cmd = 'INSERT OR IGNORE INTO ' + table_name + ' ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)'
    # sql_insert_cmd = 'INSERT OR IGNORE INTO test_sql_table ("job_name", "average_price", "skills", "job_link") VALUES (?, ?, ?, ?)'
    print('test2')
    job_content_sql.execute(sql_insert_cmd, data_list)


def look_data(table_name, connect_sql, job_content_sql):
    sql_exe = 'SELECT job_link FROM ' + table_name
    # sql_exe = 'SELECT job_link FROM test_sql_table'
    sql_commend = job_content_sql.execute(sql_exe)
    rows = sql_commend.fetchall()
    print(rows)
    for row in rows:
        print('{}\t{}'.format(row[0], row[0]))
    connect_sql.commit()

if __name__ == '__main__':
    conn_sql, job_sql = connect_database()
    table_name = 'test_sql_table'
    # create_table(table_name, conn_sql, job_sql)
    # data_1 = ['police', '40k', '', 'https://jjargkjf.com']
    # data_2 = ['engineer', '90k', 'your health', 'https://dlink.com']
    # insert_data(table_name, conn_sql, data_1)
    # insert_data(table_name, conn_sql, data_2)
    look_data(table_name, conn_sql, job_sql)
    conn_sql.commit()
    conn_sql.close()
    print('test finish')

'''
Note about this program:

We can change the string we want to be a variable, 
and then, we can change the table (or the db name we will connect) to be the function when the time we need to do,
and the SQL command can be execute correctly.
It is convenience to do something if it is variable.
'''