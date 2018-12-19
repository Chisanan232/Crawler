'''
Check proxy ip - selenium version
The program's target is check the proxy is available or not. Because I get proxy for free in web, it maybe cannot use to
crawl.
*****Addition*****
In my experience of crawl, if you use selenium package, it is very keen, I mean may be the proxy is available when you
use in like requests or pyquery packages, something else, BUT, in selenium it is not operate. I think the reason why it
happened is I use free proxy from some web so it is not stable.
'''

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Except
from selenium.webdriver.common.by import By
import random



'''1. method : function'''
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
    headers = {'User-Agent': random.choice(user_agent)}
    return headers


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


'''2. method : in popular, set directly  -  line 50, 51'''
proxy = '41.190.95.20:39544'
header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'



url = 'http://httpbin.org/get'
# url = 'http://www.youtube.com'               # Remember, if you change test-web, alter your selenium select html or css tag

options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=' + proxy)                # Directly setting
# options.add_argument('--proxy-server=%s' % get_proxy())      # By function
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
        info = driver.find_element_by_css_selector('body').text
        print(info)
except OSError as e:
    print('OSError : ', e)
except BaseException as e:
    print('Error : Oh no, it\'s fail.......')
    print('\nYour error: ', e)

driver.quit()
print('------------------------')
print('Check Finish !')
print('------------------------')
