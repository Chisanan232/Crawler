from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Except
from selenium.webdriver.common.by import By
from selenium import webdriver
from unittest import TestCase
import time



def engine_driver():
    driver = webdriver.Chrome()
    return driver

def automation_web(driver):
    url = 'https://www.google.com/search?q=michael+jordan&source=lnms&tbm=isch&sa=X&sqi=2&ved=0ahUKEwiTkP3_6dPgAhUEdt4KHWp0AmcQ_AUIDigB&biw=1536&bih=722'
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="hdtb-tls"]').click()
    driver.find_element_by_xpath('//*[@id="hdtbMenus"]/div/div[2]/div').click()
    driver.find_element_by_xpath('//*[@id="isz_lt"]/a').click()
    driver.find_element_by_xpath('//*[@id="iszlt_4mp"]').click()
    time.sleep(5)

    js = "var q=document.documentElement.scrollTop=100000"
    for i in range(0, 5):
        #将滚动条移动到页面的底部
        #Let the scoll move to the bottom in the website
        driver.execute_script(js)
        time.sleep(1)
        print('To the bottom ' + str(i) + ' time')
    Wait(driver, 5).until(Except.presence_of_all_elements_located((By.XPATH, '//*[@id="smb"]')))
    driver.find_element_by_xpath('//*[@id="smb"]').click()
    for _ in range(0, 5):
        driver.execute_script(js)
        time.sleep(1)
    # #将滚动条移动到页面的顶部
    # js = "var q=document.documentElement.scrollTop=0"
    # driver.execute_script(js)
    # time.sleep(3)
    # #若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
    # js = "var q=document.getElementById('id').scrollTop=100000"
    # # driver.execute_script(js)
    # time.sleep(3)

    # driver.close()

    print('========finish=======')

    
if __name__ == "__main__":
    browser = engine_driver()
    automation_web(browser)
