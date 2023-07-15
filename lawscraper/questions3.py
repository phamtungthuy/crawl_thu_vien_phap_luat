import os
import time
import re
import math
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

os.environ['PATH'] += r"G:\library\seleniumDriver"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
error = 0

url = f"https://thuvienphapluat.vn/cong-dong-dan-luat/dan-luat/cung-thao-luan/phong-sinh-vien-luat-113"
print(url)
driver.get(url)
driver.implicitly_wait(30)
current_file = 0
current_page = 0
def replace_special_characters(string):
    pattern = r'[^a-zA-Z0-9_]'  # Biểu thức chính quy để tìm ký tự đặc biệt
    
    return re.sub(pattern, ' ', string)

def get_questions(questions, dir_name):
    global current_file
    driver2 = webdriver.Chrome(options=options)
    driver2.maximize_window()
    driver2.implicitly_wait(30)
    for question in questions:
        link = question.get_attribute("href")
        file_name = (link.split("/")[-1]).split('.')[0]
        print(file_name)
        current_file += 1
        if os.path.exists(f'./questions/phongsinhvienluat/{dir_name}/{current_file}.html'):
            print('existed', current_file)
            continue
        try:
            print('ready')
            driver2.get(link)
            if 'error.htm' in driver2.current_url or 'checkvb.aspx' in driver2.current_url:
                print('error.html or checkvb')
                continue
            source_code = driver2.page_source
            filename = f'./questions/phongsinhvienluat/{dir_name}/{current_file}.html'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(source_code)
            
            print('saved ', filename)
        except:
            print(f'error saved file {current_file}: ', file_name)
            continue
    driver2.quit()
    
def handle_get_all_questions(f_driver, dir_name='general'):
    run = True
    wait = WebDriverWait(f_driver, 60)
    
    path = f'./questions/phongsinhvienluat/{dir_name}'
    files = os.listdir(path)
    files = [f for f in files if f.endswith('.html')]
    files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]), reverse=True)
    if files != []:
        last_file = files[0].split('.')[0]
    else: last_file = 0
    current_max_file  = int(last_file)
    current_max_page = math.ceil(current_max_file / 20)
    print('current_max_page: ', current_max_page)
    while run:
        current_url = f_driver.current_url
        print(f_driver.current_url)
        if current_url.find('check.aspx') != -1:
            
            print('check.aspx')
            # time.sleep(10)
            # f_driver.get(f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=&area=0&match=True&type=0&status=0&signer=0&sort=6&lan=1&scan=0&org=0&fields=&page={current_page}")
            break
        tmp = int(f_driver.find_element(By.CSS_SELECTOR, '.wap-pagination div p span').text.strip().split(' ')[-1].strip())
        global current_page
        print(tmp, current_page)
        if tmp <= current_page:
            global current_file
            global error
            current_file = 0
            current_page = 0
            print('current page is decreasing', error)
            error += 1
            files = os.listdir(path)
            files = [f for f in files if f.endswith('.html')]
            files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]), reverse=True)
            if files != []:
                last_file = files[0].split('.')[0]
            else: last_file = 0
            current_max_file  = int(last_file)
            current_max_page = math.ceil(current_max_file / 20)
            print('current_max_page: ', current_max_page)
            if error >= 30:
                break
        current_page = tmp
        current_file = (current_page - 1) * 20
        print('current page: ', current_page)
        print('current file:', current_file)
        
        
        
        class_attribute = f_driver.find_element(By.CSS_SELECTOR, ".page-item.active").find_element(By.XPATH, "following-sibling::*[1]").get_attribute('class')
        print(class_attribute)
        if 'disabled' in class_attribute or 'next' in class_attribute:
            print('Ket thuc')
            run = False
            break
        elif current_page < current_max_page - 1:
            print('2')
            last_tag =  f_driver.find_element(By.CSS_SELECTOR, '.page-item.next').find_element(By.XPATH, './preceding-sibling::*[1]')
            f_driver.execute_script("arguments[0].click()", last_tag)
        else:
            print('3')
            questions = f_driver.find_elements(By.CSS_SELECTOR, '#data-by-forum div.member_info p a:first-child')
            get_questions(questions, dir_name)
            next_page = f_driver.find_element(By.CSS_SELECTOR, ".page-item.active").find_element(By.XPATH, "following-sibling::*[1]")
            f_driver.execute_script("arguments[0].click();", next_page)
            try:
                wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".wap-pagination div p span"), f"Trang {current_page + 1}"))
            except:
                print('Error executing script')
                continue
        # time.sleep(3)
    print('da ra khoi vong lap')


if __name__ == '__main__':


    other_sections = driver.find_elements(By.CSS_SELECTOR, 'tbody.tablebody tr td:first-child div:first-child a')
    driver3 = webdriver.Chrome(options=options)
    driver3.maximize_window()
    driver3.implicitly_wait(30)
    
    for section in other_sections:
        dir_name = replace_special_characters(unidecode(section.text)).replace(' ', '').lower()
        pass_arrays = []
        if any(dir_name == text for text in pass_arrays):
            continue
        print(dir_name)
        dir_path = f'./questions/phongsinhvienluat/{dir_name}'
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        try:
            driver3.get(section.get_attribute("href"))
            handle_get_all_questions(driver3, dir_name)
        except:
            handle_get_all_questions(driver3, dir_name)
            print('error other sections')
        current_file = 0
        current_page = 0
    driver3.quit()
    current_file = 0
    current_page = 0
    try:
        handle_get_all_questions(f_driver=driver)
    except:
        handle_get_all_questions(f_driver=driver)
        print('error main', NameError)
    driver.quit()