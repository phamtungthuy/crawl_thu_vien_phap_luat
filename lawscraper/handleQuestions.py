from bs4 import BeautifulSoup
import json
import os
import re
import time
import glob
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
driver.implicitly_wait(30)

final_data = []
count = 0

def extract_numbers(text):
    pattern = r"(?:Điều kiện )?Điều (\d+)"
    matches = re.findall(pattern, text)
    numbers = [match for match in matches]
    return numbers

def handle_question_title(text):
    cleaned_string = re.sub(r"Điều \d+|Khoản \d+|Điểm [a-z]", "", text)
    return cleaned_string

html_files = glob.glob('./questions/**/*.html', recursive=True)

for file_path in html_files:
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

    if __name__ == '__main__':
        data = {}
        data['question_id'] = str(count + 1)
        contents = soup.select(".article__sapo.article__body > *")
        arrays = []
        for tmp in contents:
            if tmp.name and not tmp.find('img'):
                arrays.append(tmp.get_text().replace("\n", " ").strip())
        data['question'] = soup.title.string.replace('\n', ' ').replace('  ', ' ').strip()
        data['relevant_articles'] = []
        
        a_tags = soup.select(".article__sapo.article__body > * a")
        for a_tag in a_tags:
            href = a_tag["href"]
            if href.find('http') == 0:
                text = a_tag.text.strip()
                arrays = ['Chứng chỉ', "Chứng Chỉ", 'https://', 'http://', "Điều này", "Thông tư này", "Nghị định này", "Bộ luật này", 'SMART ENTERPRISE SOLUTIONS']
                if any (tmp in text for tmp in arrays):
                    continue
                law_id = ''
                for word in text.split(' '):
                    if '/' in word:
                        law_id = word
                if '/' not in law_id:
                    driver.get(href)
                    for tmp in driver.title.strip().split(' '):
                        if '/'in tmp:
                            law_id = tmp
                            # law_id = handle_question_title(text)
                    time.sleep(2)
                article_ids = extract_numbers(text)
                
                text_before_a = a_tag.previous_sibling
                if text_before_a is not None:
                    text_before_a = text_before_a.text.replace('\n\t', '').strip()
                    # position = ['tại điểm', 'tại Điểm', 'tại khoản', 'tại Khoản', 'Khoản', 'tại Điều', 'Điều', 'Căn cứ']
                    # start_position = -1
                    # for position_text in position:
                    #     start_position = text_before_a.find(position_text)
                    #     text_arrays = text_before_a[start_position:].strip().split(' ')
                    #     if(text_arrays[-1] == 'của'): text_arrays.pop()
                    #     if start_position != -1:
                    #         if position_text == 'Khoản' or position_text == 'Điều':
                    #             if text_arrays[1] == 'kiện':
                    #                 start_position = -1
                    #                 continue
                    #             article_id = ' '.join(text_arrays)
                    #         elif position_text == 'Căn cứ':
                    #             article_id = ' '.join(text_arrays[2:])
                    #         else:
                    #             article_id = ' '.join(text_arrays[1:])
                    #         break
                    # if start_position == -1:
                    #     print('title', soup.title.string)
                    #     print(f'index {index}', text_before_a)
                    article_ids = article_ids + extract_numbers(text_before_a)
                for article_id in article_ids:
                    if not any(obj['law_id'] == law_id and obj['article_id'] == article_id for obj in data['relevant_articles']):
                        data['relevant_articles'].append({
                            'law_id': law_id,
                            'article_id': article_id,
                        })
                if article_ids == []:
                    if not any(obj['law_id'] == law_id and obj['article_id'] == '' for obj in data['relevant_articles']):
                        data['relevant_articles'].append({
                            'law_id': law_id,
                            'article_id': '',
                        })
        if data['relevant_articles'] != []:
            final_data.append(data)
        count += 1
        if count == 200:
            break
        print('continuing...', count)

driver.quit()

output_file_path = './questions.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(json.dumps(final_data, ensure_ascii=False) + '\n')
print("Dữ liệu đã được ghi tiếp vào file JSON thành công.")
    

