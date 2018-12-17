from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Except
from selenium.webdriver.common.by import By
import random
import time



'''測試代理ip - selenium 版本'''

def get_header():
    user_agent = [
        # sang sung
        'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
        # sony
        'Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
        # apple iphone
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'
                  ]
    header = {'User-Agent' : random.choice(user_agent)}
    return header

def get_proxy():
    proxies = [
        '5.133.27.55:3129',
        '41.223.154.170:23500'
               ]
    # proxy = {
    #     'http://' + random.choice(proxies)
    #     # 'https://' + random.choice(proxies)
    # }
    proxy = random.choice(proxies)
    return proxy

proxy = '41.223.154.170:23500'
header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

# url = 'http://httpbin.org/get'
url = 'http://www.youtube.com'
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=' + proxy)
# options.add_argument('--proxy-server=%s' % get_proxy())
options.add_argument('--user-agent=' + header)
# options.add_argument('--user-agent=%s' % get_header())
driver = webdriver.Chrome(chrome_options=options)

try:
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(Except.presence_of_all_elements_located((By.XPATH, '//*[@id="main-message"]/h1')))
        error = driver.find_element_by_xpath('//*[@id="main-message"]/h1').text
        error_content = driver.find_element_by_xpath('//*[@id="main-message"]/p').text
        if error == '無法連上這個網站':
            print('Oh no......fail, man, please try other proxy or user agent again.')
            print(error_content)
        elif error == '沒有網際網路連線':
            print(error_content)
        else:
            print(error)
    except:
        print('success ! !')
        # info = driver.find_element_by_xpath('/html/body/pre').text
        # print(info)
except OSError as e:
    print('OSError : ', e)
except BaseException as e:
    print('fuck you error.\n')
    print(e)

print('check finish')
