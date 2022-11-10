from jobboard_scraper import JobboardScraper
from bs4 import BeautifulSoup
import time, datetime
import requests
import traceback
import json
import re


class IndeedScraper(JobboardScraper):
    def __init__(self, country, jobboard, currency):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        super().__init__(country, jobboard, currency)    

    def explore_ads_from_page(self, soup_ads_page):
        soup_ads = soup_ads_page.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result')
        if not soup_ads:
            raise Exception('There are no ads on this page')
        for soup_ad in soup_ads:
            try:
                start = time.time()
                if soup_ad.find('div', class_='title'):
                    link_ad = soup_ad.find('div', class_='title').find('a').get('href')
                    if soup_ad.find('div', class_='title').find('a').find('b'):
                        title = soup_ad.find('div', class_='title').find('a').find('b').text
                    else:
                        title = soup_ad.find('div', class_='title').find('a').text
                elif soup_ad.find('h2', class_='title'):
                    link_ad = soup_ad.find('h2', class_='title').find('a').get('href')
                    title = soup_ad.find('h2', class_='title').find('a').text
                else:
                    raise Exception("Couldn't recognize the title and/or link")
                print(link_ad)
                try:
                    company_name = soup_ad.find('span', class_='company').text
                except:
                    company_name = None
                if soup_ad.find('div', class_='recJobLoc'):
                    location_jobboard = soup_ad.find('div', class_='recJobLoc').get('data-rc-loc')
                elif soup_ad.find('span', class_='location accessible-contrast-color-location'):
                    location_jobboard = soup_ad.find('span', class_='location accessible-contrast-color-location').text
                else:
                    raise Exception("Couldn't recognize the location")
                try:
                    salary = soup_ad.find('span', class_='salaryText').text
                except:
                    salary = ''
                posting_date = soup_ad.find('span', class_='date').text
                if '30' in posting_date:
                    continue
                shortened_description = soup_ad.find('div', class_='summary').text
                employment_type = None
                if not self.exists_in_db(title, company_name, posting_date, location_jobboard):
                    time.sleep(0.5)
                    attempts = 0
                    while attempts < 2:
                        try:
                            response_ad_page = self.session.get(f'https://{self.jobboard_name}' + link_ad, headers=self.headers, timeout=(0.5, 3))
                            self.enter_log('info', f'Opened https://{self.jobboard_name}{link_ad}')
                            soup_ad_page = BeautifulSoup(response_ad_page.content, 'html.parser')
                            if not company_name and soup_ad_page.find('div', class_='jobsearch-JobMetadataHeader-itemWithIcon icl-u-textColor--secondary icl-u-xs-mt--xs') is not None:
                                company_name = 'Subcontract'
                            try:
                                if soup_ad_page.find('div', id='jobDescriptionText'):
                                    full_description = soup_ad_page.find('div', id='jobDescriptionText').text
                                else:
                                    full_description = self.get_full_desc(soup_ad_page)
                            except:
                                pass
                            try:
                                employment_type = soup_ad_page.find_all('span', class_='jobsearch-JobMetadataHeader-iconLabel')[1].text
                            except:
                                pass
                            break
                        except:
                            attempts += 1
                            if attempts > 1:
                                self.enter_log('error', f"Couldn't open https://{self.jobboard_name}{link_ad}")

                    agency_or_direct = None
                    skills = None
                    other = None
                    sector_jobboard = None
                    if not full_description:
                        full_description = 'SHORTENED DESCRIPTION  ' + shortened_description
                    # self.export_to_database(title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link_ad, other)
                else:
                    self.enter_log('info', f'https://{self.jobboard_name}{link_ad}' + ' was already in the database')
                total = time.time() - start
            except:
                pass


    def explore_ads(self):
        missed_pages = 0
        missed_cities = 0
        locations = self.locations[self.jobboard_country.lower()]
        for location, loc_details in locations.items():
            attempts_ = 0
            while attempts_ < 3:
                try:
                    print(location.upper(), '\n------------------')
                    response_location_page = self.session.get(f'https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start=0', headers=self.headers)
                    print(f'https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start=0')
                    self.enter_log('info', f'Opened https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start=0')
                    soup_location_page = BeautifulSoup(response_location_page.content, 'html.parser')
                    if soup_location_page.find('div', id='searchCountPages'):
                        num_of_ads = int(re.findall("[0-9.,]+", soup_location_page.find('div', id='searchCountPages').text)[-1].replace(',', '').replace('.', ''))
                        if num_of_ads > 999 and loc_details['neighbourhoods']:
                            for neighbourhood in loc_details['neighbourhoods']:
                                response_location_page = self.session.get(f'https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+") + "-" + neighbourhood}&radius=10&fromage=1&start=0', headers=self.headers)
                                self.enter_log('info', f'Opened https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+") + "-" + neighbourhood}&radius=10&fromage=1&start=0')
                                soup_location_page = BeautifulSoup(response_location_page.content, 'html.parser')
                                num_of_ads = int(re.findall("[0-9.,]+", soup_location_page.find('div', id='searchCountPages').text)[-1].replace(',', '').replace('.', ''))
                                self.explore_ads_from_page(soup_location_page)
                                for page_nr in range(50, num_of_ads, 50):
                                    attempts = 0
                                    while attempts < 3:
                                        try:
                                            response_location_page = self.session.get(f'https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+") + "-" + neighbourhood}&radius=10&fromage=1&start={page_nr}', headers=self.headers)
                                            self.enter_log('info', f'Opened https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+") + "-" + neighbourhood}&radius=10&fromage=1&start={page_nr}')
                                            soup_location_page = BeautifulSoup(response_location_page.content, 'html.parser')
                                            print(f'https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+") + "-" + neighbourhood}&radius=10&fromage=1&start={page_nr}')
                                            self.explore_ads_from_page(soup_location_page)
                                            print('---------------')
                                            break
                                        except:
                                            attempts += 1
                                            time.sleep(2)
                                            if attempts == 2:
                                                session = requests.Session()
                                            if attempts > 2:
                                                self.enter_log('error', f' ---- Failed at https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start={page_nr} ---- \n{traceback.format_exc()}\n--------------')
                                                print('\n----- FAILED TO OPEN PAGE -----\n')
                                                with open(f'{self.jobboard_name.replace(".", "_")}.html', 'wb') as fd:
                                                    for chunk in response_location_page.iter_content(chunk_size=128):
                                                        fd.write(chunk)
                                                missed_pages += 1
                        else:
                            self.explore_ads_from_page(soup_location_page)
                            num_of_ads = int(re.findall("[0-9.,]+", soup_location_page.find('div', id='searchCountPages').text)[-1].replace(',', '').replace('.', ''))
                            for page_nr in range(50, num_of_ads, 50):
                                attempts = 0
                                while attempts < 3:
                                    try:
                                        response_location_page = self.session.get(f'https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start={page_nr}', headers=self.headers)
                                        self.enter_log('info', f'Opened https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start={page_nr}')
                                        soup_location_page = BeautifulSoup(response_location_page.content, 'html.parser')
                                        self.explore_ads_from_page(soup_location_page)
                                        print('---------------')
                                        break
                                    except:
                                        attempts += 1
                                        time.sleep(2)
                                        if attempts == 2:
                                            session = requests.Session()
                                        if attempts > 2:
                                            self.enter_log('error', f' ---- Failed at https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start={page_nr} ---- \n{traceback.format_exc()}\n--------------')
                                            print('\n----- FAILED TO OPEN PAGE -----\n')
                                            with open(f'{self.jobboard_name.replace(".", "_")}.html', 'wb') as fd:
                                                for chunk in response_location_page.iter_content(chunk_size=128):
                                                    fd.write(chunk)
                                            missed_pages += 1
                    break
                except:
                    attempts_ += 1
                    time.sleep(2)
                    if attempts_ == 2:
                        session = requests.Session()
                    if attempts_ > 2:
                        self.enter_log('error', f' ---- Failed at https://{self.jobboard_name}/jobs?q=&l={location.replace(" ", "+")}&radius=10&fromage=1&start=0 ---- \n{traceback.format_exc()}\n--------------')
                        print('\n----- FAILED TO OPEN PAGE -----\n')
                        with open(f'{self.jobboard_name.replace(".", "_")}.html', 'wb') as fd:
                            for chunk in response_location_page.iter_content(chunk_size=128):
                                fd.write(chunk)
                        missed_cities += 1

        print(f'Missed location pages: {missed_cities}\nMissed pages: {missed_pages}')


if __name__ == "__main__":
    indeed_de = IndeedScraper('Germany', 'de.indeed.com', 'EUR')
    indeed_de.explore_ads()
