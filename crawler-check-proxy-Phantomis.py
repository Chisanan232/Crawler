'''測試代理ip - Phantomjs 版本'''
# have some strange error


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Except
from selenium.webdriver.common.by import By
import random



def get_header():
    user_agent = [
                  ]
    header = {'User-Agent' : random.choice(user_agent)}
    return header

def get_proxy():
    proxies = [
               ]
    proxy = {
        'http://' : random.choice(proxies)
        # 'https://' : random.choice(proxies)
    }
    return proxy

url = 'http://httpbin.org/get'
proxy = '178.124.71.81:8080'
header = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36'

service_args =[
    '--proxy=' + proxy,
    # '--proxy=' + get_proxy(),
    '--proxy-tyoe=http',
    '--user-agent=' + header
    # '--user-agent=' + get_header()
]
exe_path = 'C:/Users/iAirJordan/AppData/Local/Programs/Python/Python36-32/phantomjs-2.1.1-windows/bin/phantomjs.exe'
driver = webdriver.PhantomJS(service_args=service_args, executable_path=exe_path)

try:
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(Except.presence_of_all_elements_located((By.XPATH, '//*[@id="main-message"]/h1')))
        error = driver.find_element_by_xpath('//*[@id="main-message"]/h1').text
        if error == '無法連上這個網站':
            print(error+'\n')
            print('oh no....fail, man, please try other proxy or user agent again.')
    except:
        print('success ! ! !')
        info = driver.find_element_by_xpath('/html/body/pre').text
        print(info)
except OSError as e:
    print('OSError : ', e)
except:
    print('fuck you error.')