from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re
# import datetime
from datetime import date, timedelta
import time
import string 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import sys
import traceback
import datetime

def err(type, value, tb):
    print("Exception date time: {}".format(datetime.datetime.now()))
    print(traceback.print_tb(tb))

sys.excepthook = err
url = 'https://www.xn--jobbrse-stellenangebote-blc.de/jobs/berufsfeld/'

path = r'path\chromedriver.exe'
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
driver = webdriver.Chrome(executable_path=path, chrome_options=opts)
driver.maximize_window()

alpha = string.ascii_lowercase
total = []
total_offers = []
for letter in alpha[:1]:
    link = url + str(letter) + "/"
    print(letter)
    print('Litera: ', letter, link)
    session = requests.Session()            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response_obj = session.get(link, headers=headers)  
    soup_obj = BeautifulSoup(response_obj.content, 'html.parser')
    link_num = 1
    jobs = soup_obj.find_all('a', class_= 'listCols')
    for i in jobs:
        link = 'https://www.xn--jobbrse-stellenangebote-blc.de' + str(i.get('href'))
        sector_jobboard = i.text
        driver.get(link)
        print('Nr linku: ', link_num, link)
        time.sleep(2)
        czas = datetime.datetime.now()
        czas = str(czas).split(".")[0]
        print(czas)
        strona = 1
        while True:
            # table = driver.find_element_by_xpath("//div[@id='article']")
            timeout = 20
            wait = WebDriverWait(driver, timeout)
            childframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)
            table = driver.find_element_by_xpath('//*[@id="content-right"]')
            offers = table.find_elements_by_class_name('row')
            # print(len(offers))
            num = 1
            print("Strona: ", strona)
            for ad in offers:
                # print(num)
                try:
                    header = ad.find_element_by_class_name('jlcol1')
                except:
                    continue
                try:
                    header = ad.find_element_by_tag_name('a')
                except:
                    try:
                        time.sleep(2)
                        page = driver.find_element_by_tag_name('html')
                        page.send_keys(Keys.PAGE_DOWN)
                        page.send_keys(Keys.PAGE_DOWN)
                        header = ad.find_element_by_tag_name('a')
                    except:
                        try:
                            time.sleep(4)
                            page = driver.find_element_by_tag_name('html')
                            page.send_keys(Keys.END)
                            page.send_keys(Keys.PAGE_UP)
                            page.send_keys(Keys.PAGE_UP)
                            header = ad.find_element_by_tag_name('a')
                        except:
                            continue
                try:
                    link = header.get_attribute('href')
                except:
                    try:
                        time.sleep(2)
                        link = header.get_attribute('href')
                    except:
                        link = None
                # title = header.get_attribute('title')
                try:
                    title = header.text
                except:
                    try:
                        time.sleep(2)
                        page = driver.find_element_by_tag_name('html')
                        page.send_keys(Keys.PAGE_DOWN)
                        page.send_keys(Keys.PAGE_DOWN)
                        title = header.text
                    except:
                        continue
                # print(title)
                try:
                    full_description = ad.find_element_by_class_name('jobPostHeader').text.strip()
                except:
                    try:
                        time.sleep(3)
                        full_description = ad.find_element_by_class_name('jobPostHeader').text.strip()
                    except:
                        full_description = None
                
                try:
                    posting_date = ad.find_element_by_class_name('neu').text.strip()
                    p = re.compile(r'[0-9]') 
                    p = p.findall(posting_date)
                except:
                    try:
                        time.sleep(2)
                        posting_date = ad.find_element_by_class_name('neu').text.strip()
                        p = re.compile(r'[0-9]') 
                        p = p.findall(posting_date)
                    except:
                        print(num)
                        p = None
                try:
                    days = int(''.join(p))
                    posting_date = date.today() - timedelta(days)
                except:
                    posting_date = date.today()
                try:
                    company_name = ad.find_element_by_class_name('jlcol2').get_attribute('title')
                except:
                    try:
                        time.sleep(3)
                        company_name = ad.find_element_by_class_name('jlcol2').get_attribute('title')
                    except:
                        company_name = None
                salary = None
                skills = None
                location_jobboard = None
                agency_or_direct = 'Jobbrse_DE'
                employment_type = None

                new = ((title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link))
                total.append(new)
                if num == 10:
                    break
                num += 1
            page = driver.find_element_by_tag_name('html')
            page.send_keys(Keys.END)
            page.send_keys(Keys.PAGE_UP)
            page.send_keys(Keys.PAGE_UP)
            time.sleep(3)
            try:
                next_button = driver.find_element_by_class_name('pagingNext')
                next_button.click()
            except:
                break
            strona += 1

        for i in total:
            if i not in total_offers:
                total_offers.append(i)

        df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
        df.to_excel(f'Jobbrse_{str(letter)}_{str(link_num)}.xlsx')
        link_num += 1

df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
df.to_excel(f'Jobbrse_DE_all.xlsx')
