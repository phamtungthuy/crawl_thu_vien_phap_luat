import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

os.environ['PATH'] += r"G:\library\seleniumDriver"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

current_page = 1
url = f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=&area=0&match=True&type=0&status=0&signer=0&sort=6&lan=1&scan=0&org=0&fields=&page={current_page}"
print(url)
driver.get(url)
driver.implicitly_wait(30)
count = 1
max_page = 2000

def haveSomeFilesNotExist():
    for i in range(20):
        if not os.path.exists(f"./summary/page{(current_page - 1) * 20 + i + 1}.html"):
            return True
    return False

run = True
while run:
    if current_page > max_page:
        print('finished')
        break 
    current_url = driver.current_url
    current_page = int(current_url.split('=')[-1])
    print(driver.current_url)
    print('current page: ', current_page)
    if current_url.find('check.aspx') != -1:
        print('check.aspx')
        # time.sleep(10)
        # driver.get(f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=&area=0&match=True&type=0&status=0&signer=0&sort=6&lan=1&scan=0&org=0&fields=&page={current_page}")
        break
    next_page = driver.find_element(By.CSS_SELECTOR, 'div.cmPager a:last-child')
    if not haveSomeFilesNotExist():
        print('check')
        # time.sleep(3)
        next_page.click()
        continue
    laws = driver.find_elements(By.CSS_SELECTOR, 'p.nqTitle a')
    driver2 = webdriver.Chrome(options=options)
    for i in range(len(laws)):
        current_file = (current_page -1)*20 + i + 1
        if not os.path.exists(f"./summary/page{current_file}.html"):
            link = laws[i].get_attribute("href")
            try:
                driver2.get(link)
                summary_link = driver2.find_element(By.CSS_SELECTOR, '#idTabs.idTabs li:first-child a')
                driver2.execute_script("arguments[0].click();", summary_link)
                print(driver2.current_url)
                if 'error.htm' in driver2.current_url or 'checkvb.aspx' in driver2.current_url:
                    print('error.htm or checkvb')
                    continue
                filename = f'./summary/page{current_file}.html'
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(source_code)
                print(filename)
            except:
                print('error: ', current_file)
    
    
    driver2.quit()
    next_page.click()
    # time.sleep(3)
driver.quit()