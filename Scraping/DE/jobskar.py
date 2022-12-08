import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas as pd
import regex as re

import traceback
import datetime

def err(type, value, tb):
    print("Exception date time: {}".format(datetime.datetime.now()))
    print(traceback.print_tb(tb))

total = []
total_offers = []
num = 1
parts = 1
for page in range(0, 60000, 25):
    url = 'https://jobs.karriere.de/ergebnisliste.html?&of=' + str(page) + '&suid=b3b61ba4-3c28-4fcc-8822-29ef93b7effa&an=paging_next&action=paging_next'
    session = requests.Session()            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response_obj = session.get(url, headers=headers)
    soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

    print(url)
    print(datetime.datetime.now())
    try:
        table = soup_obj.find('div', class_= 'job-elements-list')
    except:
        break
    offers = table.find_all('div', recursive=False)
    for i in offers:
        title = i.find('h2', class_='job-element__body__title').text.strip()
        link = i.find('div', class_='job-element__body word-wrap').find('a').get('href')
        try:
            company_name = i.find('div', class_='job-element__body__company').text.strip()
        except:
            company_name = None
        try:
            location_jobboard = i.find('li', class_='job-element__body__location').text.strip()
        except:
            location_jobboard = None

        posting_date = i.find('time').get('data-date')
        firstDelPos = posting_date.find('T')
        posting_date = posting_date.replace(posting_date[firstDelPos:], '')

        session = requests.Session()            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        response_obj = session.get(link, headers=headers)
        soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

        content = soup_obj.find_all('main', class_= 'offer__content')
        full_description = content[1].text
        try:
            skills = content[1].find_all('section')[2].text
        except:
            skills = full_description
        agency_or_direct = 'Jobs_Karriere_DE'
        salary = None
        try:
            employment_type = soup_obj.find('li', class_='listing-list at-listing__list-icons_work-type').text.strip()
        except:
            time.sleep(2)
            try:
                employment_type = soup_obj.find('li', class_='listing-list at-listing__list-icons_work-type').text.strip()
            except:
                employment_type = None
        try:
            contract_type = soup_obj.find('li', class_='listing-list at-listing__list-icons_contract-type').text.strip()
        except:
            time.sleep(2)
            try:
                contract_type = soup_obj.find('li', class_='listing-list at-listing__list-icons_contract-type').text.strip()
            except:
                contract_type = None
        sector_jobboard = None

        print(num)
        num += 1
        new = ((title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, contract_type, full_description, skills, link))
        total.append(new)

    for i in total:
        if i not in total_offers:
            total_offers.append(i)
    if num in range(0, 60000, 100):
        df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Contract Type', 'Description', 'Skills', 'Link'])
        df.to_excel(f'Jobs_Karriere_DE{str(parts)}.xlsx')
        parts += 1
        print(datetime.datetime.now())
df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Contract Type', 'Description', 'Skills', 'Link'])
df.to_excel(f'Jobs_Karriere_DE.xlsx')