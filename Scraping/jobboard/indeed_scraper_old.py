from jobboard_scraper import JobboardScraper
from bs4 import BeautifulSoup
import time, datetime
import requests
import traceback


class IndeedScraper(JobboardScraper):

    def explore_ads(self):
        try:
            missed_ads = 0
            missed_pages = 0
            missed_province_pages = 0
            missed_subsector_pages = 0
            missed_sector_pages = 0
            session = requests.Session()
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response_main_page = session.get(f'https://{self.jobboard_name}/browsejobs', headers=headers)
            self.enter_log('info', f'Opened https://{self.jobboard_name}/browsejobs')
            soup_main_page = BeautifulSoup(response_main_page.content, 'html.parser')
            soup_sectors = soup_main_page.find('table', id='categories').find_all('a')
            for soup_sector in soup_sectors[::-1]:
                name_sector = soup_sector.text
                link_sector = f'https://{self.jobboard_name}' + soup_sector.get('href')
                print(link_sector)
                print('----')
                attempts____ = 0
                while attempts____ < 4:
                    try:
                        response_sector_page = session.get(link_sector, headers=headers)
                        self.enter_log('info', f'Opened {link_sector}')
                        soup_sector_page = BeautifulSoup(response_sector_page.content, 'html.parser')
                        soup_subsectors = soup_sector_page.find('table', id='titles').find_all('p', class_='actions')
                        for soup_subsector in soup_subsectors:
                            link_subsector = f'https://{self.jobboard_name}' + soup_subsector.find('a').get('href')
                            print(link_subsector)
                            print('---')
                            attempts___ = 0
                            while attempts___ < 4:
                                try:
                                    response_subsector_page = session.get(link_subsector, headers=headers, timeout=(2, 10))
                                    self.enter_log('info', f'Opened {link_subsector}')
                                    soup_subsector_page = BeautifulSoup(response_subsector_page.content, 'html.parser')
                                    soup_provinces = soup_subsector_page.find('table', id='states').find_all('a')
                                    for soup_province in soup_provinces:
                                        link_cities_page = f'https://{self.jobboard_name}' + soup_province.get('href')
                                        print(link_cities_page)
                                        print('--')
                                        attempts__ = 0
                                        while attempts__ < 4:
                                            try:
                                                response_cities_page = session.get(link_cities_page, headers=headers, timeout=(2, 10))
                                                self.enter_log('info', f"Opened {link_cities_page}")
                                                soup_cities_page = BeautifulSoup(response_cities_page.content, 'html.parser')
                                                link_ads_page = soup_cities_page.find('table', id='browsejobs_main_content').find('h1').find('a').get('href') + '&fromage=3'
                                                print(link_ads_page)
                                                print('-')
                                                while True:
                                                    attempts_ = 0
                                                    while attempts_ < 4:
                                                        try:
                                                            response_ads_page = session.get(f'https://{self.jobboard_name}' + link_ads_page, headers=headers, timeout=(1, 10))
                                                            self.enter_log('info', f'Opened https://{self.jobboard_name}' + link_ads_page)
                                                            self.enter_log('info', str(datetime.datetime.now()))
                                                            soup_ads_page = BeautifulSoup(response_ads_page.content, 'html.parser')
                                                            soup_ads = soup_ads_page.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result')
                                                            if not soup_ads:
                                                                raise Exception('There are no ads on this page')
                                                            for soup_ad in soup_ads:
                                                                try:
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
                                                                        raise Exception
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
                                                                        raise Exception
                                                                    try:
                                                                        salary = soup_ad.find('span', class_='salaryText').text
                                                                    except:
                                                                        salary = ''
                                                                    posting_date = soup_ad.find('span', class_='date').text
                                                                    if '30' in posting_date:
                                                                        continue
                                                                    shortened_description = soup_ad.find('div', class_='summary').text
                                                                    if not self.exists_in_db(title, company_name, posting_date, location_jobboard):
                                                                        time.sleep(0.9)
                                                                        attempts = 0
                                                                        while attempts < 2:
                                                                            try:
                                                                                response_ad_page = session.get(f'https://{self.jobboard_name}' + link_ad, headers=headers, timeout=(0.5, 3))
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
                                                                                    full_description = 'SHORTENED DESCRIPTION  ' + shortened_description
                                                                                try:
                                                                                    employment_type = soup_ad_page.find_all('span', class_='jobsearch-JobMetadataHeader-iconLabel')[1].text
                                                                                except:
                                                                                    employment_type = None
                                                                                break
                                                                            except:
                                                                                attempts += 1
                                                                                if attempts > 1:
                                                                                    self.enter_log('error', f"Couldn't open https://{self.jobboard_name}{link_ad}")

                                                                        agency_or_direct = None
                                                                        skills = None
                                                                        other = None

                                                                        sector_jobboard = name_sector
                                                                        self.export_to_database(title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link_ad, other)
                                                                    else:
                                                                        self.enter_log('info', f'https://{self.jobboard_name}{link_ad}' + ' was already in the database')
                                                                except:
                                                                    self.enter_log('error', f'Failed analyzing {soup_ad.text}\nfrom: {link_ads_page}\n{traceback.format_exc()}')
                                                            break
                                                        except:
                                                            attempts_ += 1
                                                            time.sleep(2)
                                                            if attempts_ > 1:
                                                                session = requests.Session()
                                                            if attempts_ > 2:
                                                                self.enter_log('error', f"Failet at https://{self.jobboard_name}{link_ads_page}\n{traceback.format_exc()}")
                                                                missed_pages += 1
                                                    next_page = ['Volgende', 'Next', 'Weiter', 'Następna', 'Prossima', 'Suivant', 'Siguiente']
                                                    if soup_ads_page.find('ul', class_='pagination-list').find_all('li')[-1].find('span', class_='np'):
                                                        link_ads_page = soup_ads_page.find('ul', class_='pagination-list').find_all('li')[-1].find('a').get('href')
                                                    elif soup_ads_page.find('div', class_='pagination') and any(n in soup_ads_page.find('div', class_='pagination').find('span', class_='np').text for n in next_page):
                                                        link_ads_page = soup_ads_page.find('div', class_='pagination').find_all('a')[-1].get('href')
                                                    else:
                                                        break
                                                break
                                            except:
                                                attempts__ += 1
                                                time.sleep(3)
                                                if attempts__ > 1:
                                                    session = requests.Session()
                                                if attempts__ > 2:
                                                    self.enter_log('error', f' ---- Failed at {link_cities_page} (province page) ---- \n{traceback.format_exc()}\n--------------')
                                                    print('\n----- FAILED TO OPEN PROVINCE PAGE -----\n')
                                                    with open(f'{self.jobboard_name.replace(".", "_")}.html', 'wb') as fd:
                                                        for chunk in response_cities_page.iter_content(chunk_size=128):
                                                            fd.write(chunk)
                                                    missed_province_pages += 1
                                    break
                                except:
                                    attempts___ += 1
                                    time.sleep(3)
                                    if attempts___ > 1:
                                        session = requests.Session()
                                    if attempts___ > 2:
                                        self.enter_log('error', f' ---- Failed at {link_subsector} (subsector page) ---- \n{traceback.format_exc()}\n--------------')
                                        print('\n----- FAILED TO OPEN SUBSECTOR PAGE -----\n')
                                        with open(f'{self.jobboard_name.replace(".", "_")}_subsector.html', 'wb') as fd:
                                            for chunk in response_cities_page.iter_content(chunk_size=128):
                                                fd.write(chunk)
                                        missed_subsector_pages += 1
                        break
                    except:
                        attempts____ += 1
                        time.sleep(3)
                        if attempts____ > 1:
                            session = requests.Session()
                        if attempts___ > 2:
                            self.enter_log('error', f' ---- Failed at {link_sector} (subsector page) ---- \n{traceback.format_exc()}\n--------------')
                            print('\n----- FAILED TO OPEN SECTOR PAGE -----\n')
                            with open(f'{self.jobboard_name.replace(".", "_")}_sector.html', 'wb') as fd:
                                for chunk in response_cities_page.iter_content(chunk_size=128):
                                    fd.write(chunk)
                            missed_sector_pages += 1

            self.enter_log('info', f"Missed ads: {str(missed_ads)},\nmissed pages: {str(missed_pages)},\nmissed province pages: {str(missed_province_pages)},\nmissed subsector pages: {str(missed_subsector_pages)}")
            self.enter_log('info', f'Scraping ended at {str(datetime.datetime.now())}')
            self.close_db_cnxn()
        except:
            self.send_email(f'{self.jobboard_name} scraper failed', f'Indeed scraper failed at sector {name_sector}\n{traceback.format_exc()}')


if __name__ == "__main__":
    indeed_de = IndeedScraper('Germany', 'de.indeed.com', 'EUR')
    indeed_de.explore_ads()