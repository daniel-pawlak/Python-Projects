import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re
from datetime import date, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

url = 'https://www.jobanzeigen.de/'

path = r'C:\Users\tobiasz\Desktop\VS Code\chromedriver.exe'
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
driver = webdriver.Chrome(executable_path=path, chrome_options=opts)

session = requests.Session()            
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
response_obj = session.get(url, headers=headers)
soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

table = soup_obj.find('div', class_='job-industry-list ci-industry-stats')
jobs = table.find_all('div', class_='job-industry')

total = []
total_offers = []
link_num = 1
for i in jobs[1:]:
    head = i.find('a')
    url = 'https://www.jobanzeigen.de' + head.get('href') + '?page=' 
    sector_jobboard = head.text
    print(url, sector_jobboard)
    page = 1
    num = 1
    while True:
        link2 = url + str(page)
        print('Strona: ', page)
        driver.get(link2)
        driver.maximize_window()
        time.sleep(1)

        try:
            cookie = driver.find_element_by_xpath('//*[@id="consentDialog"]/div[2]/div[2]/div/div[2]/div[1]/div/div')
            cookie.click()
        except:
            None
        offers = driver.find_elements_by_tag_name('article')
        if len(offers) == 0:
            break
        for offer in offers:
            title = offer.find_element_by_tag_name('h2').text.replace('NEU', '').replace('TOP-JOB', '').strip()
            link = offer.find_element_by_tag_name('a').get_attribute('href')
            link = link.replace('https://clickout.classmarkets.com/clickout?url=', '')
            print(num, title)
            bottom = offer.find_element_by_class_name('vacancy__location')
            try:
                location_jobboard = bottom.find_element_by_class_name('vacancy__city').text.replace(',', '').strip()
            except:
                location_jobboard = None
            company_name = bottom.text
            try:
                firstDelPos = company_name.find(',')
                company_name = company_name.replace(company_name[:firstDelPos+1], '').replace('AT, DE, ', '').strip()
            except: 
                company_name = None
                print('brak company')

            print(company_name)
            posting_date = offer.find_element_by_class_name('vacancy__date').text.replace('veröffentlicht am','').strip()

            try:
                time.sleep(2)
                session = requests.Session()            
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
                response_obj1 = session.get(link, headers=headers)
                soup_obj1 = BeautifulSoup(response_obj1.content, 'html.parser')
                left_box = soup_obj1.find('div', class_= 'panel-panel panel-col job-back-button-processed')

                try:
                    employment_type = left_box.find('div', class_= 'panel-pane pane-entity-field pane-node-field-job-employment-type-term').text.strip()
                except:
                    employment_type = None
                
                full_description = soup_obj1.find('body').text.strip()
            except:
                full_description = None
            
            agency_or_direct = 'Jobanzeigen_DE'
            salary = None
            skills = None

            num += 1
            new = ((title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link))
            total.append(new)
        page += 1
        for i in total:
            if i not in total_offers:
                total_offers.append(i)

        df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
        df.to_excel(f'Jobzeigen_{str(link_num)}.xlsx')
    link_num += 1
df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
df.to_excel(f'Jobzeigen_DE_all.xlsx')