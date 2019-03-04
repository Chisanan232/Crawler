from selenium import webdriver
import time



driver = webdriver.Chrome()

url = 'https://www.google.com/search?q=michael+jordan&source=lnms&tbm=isch&sa=X&sqi=2&ved=0ahUKEwiTkP3_6dPgAhUEdt4KHWp0AmcQ_AUIDigB&biw=1536&bih=722'
driver.get(url)

for i in range(0, 10):
    #将滚动条移动到页面的底部
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(1)
    print('To the bottom ' + str(i) + ' time')
# #将滚动条移动到页面的顶部
# js = "var q=document.documentElement.scrollTop=0"
# driver.execute_script(js)
# time.sleep(3)
# #若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
# js = "var q=document.getElementById('id').scrollTop=100000"
# # driver.execute_script(js)
# time.sleep(3)

driver.close()

print('========finish=======')
