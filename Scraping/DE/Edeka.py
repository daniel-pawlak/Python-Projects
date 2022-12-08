from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import regex as re

url = 'https://verbund.edeka/karriere/stellenb%C3%B6rse/#/?levels=27412,27413,27414,27411'

path = r'path\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.get(url)
time.sleep(1)

cookies = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[2]')
cookies.click()

driver.maximize_window()
time.sleep(1)
table = driver.find_element_by_class_name('o-job-board__results-l__wrapper')
offers = table.find_elements_by_class_name('o-job-board__results-l__entry')

total = []
num = 3901  # zmienione, by zaczac scrapowac od tego miejsca
number = driver.find_element_by_xpath('/html[1]/body[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span[1]').text
number = int(number.replace(',', ''))
print(number)
input()
while num != number:
    table = driver.find_element_by_class_name('o-job-board__results-l__wrapper')
    offers = table.find_elements_by_class_name('o-job-board__results-l__entry')
    for i in offers:
        header = i.find_element_by_tag_name('a')
        link = header.get_attribute('href')
        title = header.text.strip()
        company_name = i.find_element_by_class_name('o-job-board__results-l__company-body').text.strip()
        location_jobboard = i.find_element_by_class_name('o-job-board__results-l__location-body').text.strip()
        
        driver.execute_script("window.open('');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)
     
        box = driver.find_element_by_class_name('o-m402-job-quick-facts__wrapper').find_elements_by_tag_name('div')

        try:
            employment_type = box[2].text.replace('Beschäftigungsart', '').strip()
        except:
            employment_type = None
        try:
            sector_jobboard = box[3].text.replace('Tätigkeitsfeld', '').strip()
        except:
            sector_jobboard = None

        posting_date = None
        try:
            full_description = driver.find_element_by_class_name('o-m201-job-copy__inner').text
        except:
            full_description = None
        try:
            skills = driver.find_elements_by_class_name('o-m201-job-copy__item')[1].text
        except:
            skills = None    
        agency_or_direct = None
        salary = None

        driver.execute_script("window.close('');")
        driver.switch_to.window(driver.window_handles[0])
 
        new = ((title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link))
        total.append(new)
        num += 1
        print(num)

        if num in range(1, 7000, 100):
            dfp = pd.DataFrame(total, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
            dfp.to_excel('Edeka_parts.xlsx')

    page = driver.find_element_by_tag_name('html')
    page.send_keys(Keys.PAGE_DOWN)
    try:
        button = driver.find_element_by_xpath('//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[1]/button[2]/span[1]/*[1]')
        button.click()
    except:
        input()
        button = driver.find_element_by_xpath('//body/div[2]/div[3]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[1]/button[2]/span[1]/*[1]')
        button.click()
    page = driver.find_element_by_tag_name('html')
    page.send_keys(Keys.PAGE_UP)
df = pd.DataFrame(total, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
df.to_excel('Edeka.xlsx') 
