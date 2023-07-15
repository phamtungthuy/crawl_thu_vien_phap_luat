import os
import time
import re
import math
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys

# os.environ['PATH'] += r"G:\library\seleniumDriver"
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)

# driver.get("https://thuvienphapluat.vn/cong-dong-dan-luat/dan-luat/cung-thao-luan/vuong-mac-phap-ly-111")
# element = driver.find_element(By.CSS_SELECTOR, ".page-item.active").find_element(By.XPATH, "following-sibling::*[1]")
# print(element.get_attribute('class'))
# driver.execute_script("arguments[0].click();", element)
# # element.click()

arr = []
tmp = 0
count = 0
for i in range(300001, 305817):
    if not os.path.exists(f'./total/page{i}.html'):
        print(i)
        count += 1
        if math.ceil(i / 20) not in arr:
            tmp = math.ceil(i / 20)
            arr.append(tmp)
print(arr)
# print(arr)
print(count)
# path = './questions/duthaoluatmoi/general'
# files = os.listdir(path)
# files = [f for f in files if f.endswith('.html')]
# files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]), reverse=True)
# last_file = files[0].split('.')[0]
# print(last_file)
# print(math.ceil(int(last_file) / 20))
# arr = []
# for i in range(93001, 94001):
#     file_path = f'./total/page{i}.html'
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             html_content = file.read()
#         soup = BeautifulSoup(html_content, 'html.parser')
#         element = soup.select('.ghd.ghdm.ghdmbdr')
#         print('continuing ', i)
#         if element is None:
#             print(file_path)
#             arr.append(i)
# print(arr)