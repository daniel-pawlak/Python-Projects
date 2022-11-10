# -*- coding: utf-8 -*-
# this one is useful
from datetime import datetime, timedelta, date
from unidecode import unidecode
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openpyxl import Workbook
from difflib import SequenceMatcher
from langdetect import detect, detect_langs
from flashtext import KeywordProcessor
from itertools import chain
import traceback
import json
import functools
import time
import logging
import smtplib
import requests
import pyodbc
import re
import io


class JobboardScraper:

    def __init__(self, country, jobboard, currency):
        self.skills_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\skills.txt'
        self.db_config_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\db_config.json'
        self.locations_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\locations.json'
        self.companies_sectors_map_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\companies_sectors_map.json'
        self.companies_sectors_linkedin_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\companies_sectors_linkedin_shaved.json'
        self.isco_jobtitles_en_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\isco_jobtitles_en.json'
        self.isco_jobtitles_de_fr_it_path = r'C:\Users\danie\Desktop\Python\Praca\Jobboard\isco_jobtitles_de_fr_it.json'

        # self.skills_path = r'/home/tobiasz/python_scripts/skills.txt'
        # self.db_config_path = r'/home/tobiasz/python_scripts/db_config.json'
        # self.locations_path = r'/home/tobiasz/python_scripts/locations.json'
        # self.companies_sectors_map_path = r'/home/tobiasz/python_scripts/companies_sectors_map.json'
        # self.companies_sectors_linkedin_path = r'/home/tobiasz/python_scripts/companies_sectors_linkedin_shaved.json'
        # self.isco_jobtitles_en_path = r'/home/tobiasz/python_scripts/isco_jobtitles_en.json'
        # self.isco_jobtitles_de_fr_it_path = r'/home/tobiasz/python_scripts/isco_jobtitles_de_fr_it.json'

        self.jobboard_country = country
        self.jobboard_name = jobboard
        self.salary_currency = currency
        self.year = ['annum', 'year', 'annual', 'yaar', 'jaarlijks', 'rocznie', 'rok', 'jahr', 'anno', 'ano', 'anualmente', 'annee', 'annuellement', 'arligen']
        self.month = ['month', 'maand', 'monat', 'mies', 'manad', 'mois', 'mensuel', 'mes', 'mensual', 'mese', 'mensile']
        self.week = ['week', 'wekelijks', 'woche', 'tydzien', 'tyg', 'settimanale', 'semanal', 'hebdomadaire', 'vecka']
        self.day = ['day', 'daily', 'dag', 'tag', 'dzien', 'jour', 'dia', 'giorno']
        self.hour = ['hour', 'uur', 'uhr', 'godz', 'hora', 'timme', 'heure', 'ora', 'stunde']
        self.excluded_words = ['UEFA', 'Umsatz', 'EUROPAGES', 'Milliarden', 'EUREF', 'EURO 2020', 'Mio.']
        self.salary_words = ['salary', 'lohn', 'rate', 'gehalt', 'salaire', 'traitement', 'salario', 'sueldo', 'stipendio', 'salario', 'mensile', 'lön', 'pensja', 'wypłata']
        self.glassdoor_gics_dict = {
            'Energy':['Energy', 'Oil & Gas Exploration & Production', 'Oil & Gas Services'],
            'Materials':['Mining'],
            'Industrials':['Aerospace & Defense', 'Airlines', 'Architectural & Engineering Services', 'Building & Personnel Services', 'Business Service Centers & Copy Shops', 'Chemical Manufacturing', 'Commerical Equipment Rental', 'Construction', 'Express Delivery Services', 'Industrial Manufacturing', 'Logistics & Supply Chain', 'Miscellaneous Manufacturing', 'Office Supply Stores', 'Rail', 'Research & Development', 'Security Services', 'Staffing & Outsourcing', 'Telecommunications Manufacturing', 'Transportation Equipment Manufacturing', 'Transportation Management', 'Truck Rental & Leasing', 'Trucking'],
            'Consumer Discretionary':['Automotive Parts & Accessories Stores', 'Beauty & Personal Accessories Stores', 'Car Rental', 'Casual Restaurants', 'Catering & Food Service Contractors', 'Colleges & Universities', 'Consumer Electronics & Appliances Stores', 'Consumer Product Rental', 'Consumer Products Manufacturing', 'Convenience Stores & Truck Stops', 'Department, Clothing, & Shoe Stores', 'Drug & Health Stores', 'Education Training Services', 'Fast-Food & Quick-Service Restaurants', 'Food & Beverage Stores', 'Funeral Services', 'Gambling', 'Gas Stations', 'General Merchandise & Superstores', 'General Repair & Maintenance', 'Grocery Stores & Supermarkets', 'Auto Repair & Maintenance', 'Health, Beauty, & Fitness', 'Home Centers & Hardware Stores', 'Home Furniture & Housewares Stores', 'Hotels, Motels, & Resorts', 'K-12 Education', 'Legal', 'Media & Entertainment Retail Stores', 'Membership Organizations', 'Other Retail Stores', 'Parking Lots & Garages', 'Preschool & Child Care', 'Sporting goods Stores', 'Sports & Recreation', 'Toy & Hobby Stores', 'Travel Agencies', 'Upscale Restaurants', 'Vehicle Dealers', 'Wholesale'],
            'Consumer Staples':['Food & Beverage Manufacturing', 'Food Production'],
            'Health Care':['Biotech & Pharmaceuticals', 'Health Care Products Manufacturing', 'Health Care Services & Hospitals'],
            'Financials':['Accounting', 'Banks & Credit Unions', 'Brokerage Services', 'Financial Analytics & Research', 'Financial Transaction Processing', 'Insurance Agencies & Brokerages', 'Insurance Carriers', 'Investment Banking & Asset Management', 'Lending'],
            'Information Technology':['Computer Hardware & Software', 'Enterprise Software & Network Solutions', 'IT Services', 'Internet', 'Electrical & Electronic Manufacturing'],
            'Communication Services':['Advertising & Marketing', 'Cable, Internet & Telephone Providers', 'Motion Picture Production & Distribution', 'News Outlet', 'Publishing', 'Radio', 'TV Broadcast & Cable Networks', 'Telecommunications Services', 'Video Games'],
            'Utilities':['Utilities'],
            'Real Estate':['Real Estate'],
            'Government & Public Services':['Federal Agencies', 'Municipal Governments', 'Social Assistance', 'State & Regional Agencies']
        }
        self.linkedin_gics_dict = {
            'Energy':['Oil & Energy'],
            'Materials':['Chemicals', 'Mining & Metals', 'Building Materials', 'Plastics', 'Paper & Forest Products', 'Glass, Ceramics & Concrete'],
            'Industrials':['Construction', 'Mechanical or Industrial Engineering', 'Electrical & Electronic Manufacturing', 'Human Resources', 'Transportation/Trucking/Railroad', 'Management Consulting', 'Civil Engineering', 'Design', 'Research', 'Logistics & Supply Chain', 'Architecture & Planning', 'Facilities Services', 'Machinery', 'Airlines/Aviation', 'Enviromental Services', 'Aviation and Aerospace', 'Staffing & Recruiting', 'Industrial Automation', 'Graphic Design', 'Security & Investigations', 'Import and Export', 'Public Relations and Communications', 'Business Supplies & Equipment', 'International Trade and Development', 'Events Services', 'Renewables & Envirnoment', 'Defense & Space', 'Printing', 'Maritime', 'Outsourcing/Offshoring', 'Warehousing', 'Program Development', 'Packaging and Containers', 'Market Research', 'Translation & Localisation', 'Package/Freight Delivery', 'Shipbuilding', 'Railroad Manufacture', 'Nanotechnology'],
            'Consumer Discretionary':['Education Management', 'Retail', 'Automotive', 'Higher Education', 'Health, Welness & Fitness', 'Hospitality', 'Primary/Secondary Education', 'Consumer Services', 'Restaurants', 'Law Practice', 'Apparel & Fashion', 'Consumer Goods', 'Entertainment', 'Arts & Crafts', 'Wholesale', 'Legal Services', 'Leisure, Travel & Turism', 'Sporting Goods', 'Music', 'Professional Training & Coaching', 'Individual & Family Services', 'Cosmetics', 'Textiles', 'Consumer Elecronics', 'Photography', 'Furniture', 'Fine Art', 'E-learning', 'Supermarkets', 'Performing Arts', 'Luxury Goods & Jewelry', 'Recreational Facilities & Services', 'Sporting Goods', 'Libraries', 'Gambling & Casinos'],
            'Consumer Staples':['Food & Beverages', 'Food Production', 'Farming', 'Wine & Spirits', 'Ranching', 'Dairy', 'Fishery', 'Tobacco'],
            'Health Care':['Hospital & Health Care', 'Medical Practice', 'Pharmaceuticals', 'Medical Devices', 'Mental Health Care', 'Biotechnology', 'Alternative Medicine', 'Veterinary'],
            'Financials':['Financial Services', 'Accounting', 'Banking', 'Insurance', 'Investment Management', 'Investment Banking', 'Capital Markets', 'Venture Capital & Private Equity'],
            'Information Technology':['Information Technology and Services', 'Computer Software', 'Internet', 'Computer Networking', 'Computer Hardware', 'Computer & Network Security', 'Semiconductors'],
            'Communication Services':['Marketing & Advertising', 'Telecommunications', 'Broadcast Media', 'Media Production', 'Writing & Editing', 'Publishing', 'Information Services', 'Online Media', 'Computer Games', 'Animation', 'Motion Pictures & Film', 'Newspapers', 'Wireless'],
            'Utilities':['Utilities'],
            'Real Estate':['Real Estate', 'Commercial Real Estate'],
            'Government & Public Services':['Government Administration', 'Military', 'Law Enforcement', 'Executive Office', 'Government Relations', 'Public Safety', 'Judiciary', 'International Affairs', 'Public Policy', 'Museums and Institutions', 'Political Organization', 'Alternative Dispute Resolution', 'Legislative Office'],
            'Non-profit':['Non-profit Organization Management', 'Civic and Social Organization', 'Religious Institutions', 'Philanthropy', 'Think Thanks', 'Fund-Raising']
        }
        with open(self.skills_path, 'r', encoding='utf8') as f:
            self.skills_list = f.read()
            self.skills_list = self.skills_list.split('\n')
            self.skills_keyword_processor_short = KeywordProcessor(case_sensitive=True)
            self.skills_keyword_processor_long = KeywordProcessor(case_sensitive=False)
            for skill in self.skills_list:
                if len(skill.strip()) > 4:
                    self.skills_keyword_processor_long.add_keyword(skill.strip())
                else:
                    self.skills_keyword_processor_short.add_keyword(skill.strip())
        # with open(self.db_config_path, 'r', encoding='utf8') as f:
        #     self.db_config = json.load(f)
        # self.cnxn = pyodbc.connect('DRIVER='+self.db_config['driver']+';SERVER='+self.db_config['server']+';PORT=1433;DATABASE='+self.db_config['database']+';UID='+self.db_config['username']+';PWD='+self.db_config['password'])
        with open(self.locations_path, 'r', encoding='utf8') as f:
            self.locations = json.load(f)
            for country, country_data in self.locations.items():
                for city, city_data in self.locations[country].items():
                    self.locations[country][city]['name_flashtext'] = KeywordProcessor()
                    self.locations[country][city]['name_flashtext'].add_keyword(city.lower())
                    self.locations[country][city]['zip_codes_flashtext'] = KeywordProcessor()
                    for x in self.locations[country][city]['zip_codes']: self.locations[country][city]['zip_codes_flashtext'].add_keyword(x.lower())
                    self.locations[country][city]['neighbourhoods_flashtext'] = KeywordProcessor()
                    for x in self.locations[country][city]['neighbourhoods']: self.locations[country][city]['neighbourhoods_flashtext'].add_keyword(x.lower())
                    self.locations[country][city]['other_names_flashtext'] = KeywordProcessor()
                    for x in self.locations[country][city]['other_names']: self.locations[country][city]['other_names_flashtext'].add_keyword(x.lower())

        with open(self.companies_sectors_map_path, 'r', encoding='utf8') as companies_sectors_f:
            self.companies_sectors = json.load(companies_sectors_f)
        with open(self.companies_sectors_linkedin_path, 'r', encoding='utf8') as f:
            self.companies_sectors_linkedin = json.load(f)
        with open(self.isco_jobtitles_en_path, 'r', encoding='utf-8') as f:
            self.jobtitles_en = json.load(f)
        with open(self.isco_jobtitles_de_fr_it_path, 'r', encoding='utf-8') as f:
            self.jobtitles_de_fr_it = json.load(f)
        for language in ['de', 'fr', 'it']:
            for major, sub_majors in self.jobtitles_de_fr_it[language].items():
                for sub_major, minors in sub_majors[0].items():
                    for minor, unit_groups in minors[0].items():
                        for unit_group in unit_groups[0]:
                            temp_ug = []
                            for a in unit_groups[0][unit_group][0]:
                                a = re.split("[#/,;: )(-]", a)
                                temp_ug += a
                            for x in temp_ug.copy():
                                if len(x) < 3 or (len(x) < 5 and not x == x.upper()):
                                    temp_ug.remove(x)
                            unit_groups[0][unit_group][0] = [unit_groups[0][unit_group][0], list(set([x.lower() for x in temp_ug]))]

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename=f"{str(datetime.today().strftime('%Y-%m-%d'))}_{self.jobboard_name.replace('.', '_')}_logs.log", level=logging.INFO, format=LOG_FORMAT)
        logging.info(f'Scraping started')
        if currency != 'EUR':
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get('https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html', headers=headers)
            soup_obj = BeautifulSoup(response.content, 'html.parser')
            table = soup_obj.find('tbody')
            page_currencies = table.find_all('tr')
            for cur in page_currencies:
                if cur.find('td', class_='currency').get('id') == currency:
                    self.currency_rate = round(float(cur.find('span', class_='rate').text), 2)
        else:
            self.currency_rate = 1


    # def timer(f):
    #     @functools.wraps(f)
    #     def wrapper(self, *args, **kwargs):
    #         start = time.time()
    #         rv = f(self, *args, **kwargs)
    #         total = time.time() - start
    #         print("Time:" , total)
    #         return rv
    #     return wrapper


    # Returns title and title according to ISCO08
    def __parse_title(self, title, simple_parsing=False):
        isco08_major = None
        isco08_submajor = None
        isco08_minor = None
        isco08_unit_group = None
        title_custom = None
        if not simple_parsing:
            if title:
                promoted_languages = {'de':['Germany', 'Switzerland', 'Austria'], 'fr':['France', 'Switzerland', 'Canada', 'Belgium'], 'it':['Italy', 'Switzerland']}
                title_lang = ''
                highest = 0
                for lang, countries in promoted_languages.items():
                    if self.jobboard_country in countries:
                        for detected_lang in detect_langs(title):
                            if (detected_lang.prob + 0.2) > highest and detected_lang.lang == lang:
                                highest = detected_lang.prob + 0.2
                                title_lang = detected_lang.lang
                if any(x == title_lang for x in ['de', 'fr', 'it']):
                    highest = [0, [None, None, None, None]]
                    found = None
                    for major, sub_majors in self.jobtitles_de_fr_it[title_lang].items():
                        for sub_major, minors in sub_majors[0].items():
                            for minor, unit_groups in minors[0].items():
                                for unit_group in unit_groups[0]:
                                    if any(x in title.lower() for x in unit_groups[0][unit_group][0][1]):
                                        found = [x for x in unit_groups[0][unit_group][0][1] if x in title.lower()]
                                        similarity = 0
                                        for f in found:
                                            for oj_word in re.split("[#/,;: \)\(-]", title):
                                                if SequenceMatcher(None, oj_word.lower(), f).ratio() > 0.8:
                                                    multiplier = len([x for x in unit_groups[0][unit_group][1] if SequenceMatcher(None, x.lower(), oj_word.lower()).ratio() > 0.9]) + len([x for x in minors[1] if SequenceMatcher(None, x.lower(), oj_word.lower()).ratio() > 0.9]) + len([x for x in sub_majors[1] if SequenceMatcher(None, x.lower(), oj_word.lower()).ratio() > 0.9]) + 1
                                                    divider = len([x for x in unit_groups[0][unit_group][2] if SequenceMatcher(None, x.lower(), oj_word.lower()).ratio() > 0.9]) + len([x for x in minors[2] if SequenceMatcher(None, x.lower(), oj_word.lower()).ratio() > 0.9]) + len([x for x in sub_majors[2] if SequenceMatcher(None, x.lower(), oj_word.lower()).ratio() > 0.9]) + 1
                                                    similarity += SequenceMatcher(None, oj_word.lower(), f).ratio() * multiplier / divider
                                        if similarity > highest[0]:
                                            highest = (similarity, (major, sub_major, minor, unit_group))
                    isco08_major = highest[1][0]
                    isco08_submajor = highest[1][1]
                    isco08_minor = highest[1][2]
                    isco08_unit_group = highest[1][3]
                elif detect_langs(title)[0].lang == 'en':
                    highest = [0, [None, None, None, None]]
                    for major, sub_majors in self.jobtitles_en.items():
                        for sub_major, minors in sub_majors.items():
                            for minor, unit_groups in minors.items():
                                for unit_group in unit_groups:
                                    if any([x for x in unit_groups[unit_group][0] if re.search(f'\\b{x.lower()}\\b', title.lower())]) and any([x for x in unit_groups[unit_group][1] if re.search(f'\\b{x.lower()}\\b', title.lower())]):
                                        similarity = len([x for x in unit_groups[unit_group][0] + unit_groups[unit_group][1] if re.search(f'\\b{x.lower()}\\b', title.lower())]) * 3
                                    elif any([x for x in unit_groups[unit_group][0] if re.search(f'\\b{x.lower()}\\b', title.lower())]):
                                        similarity = len([x for x in unit_groups[unit_group][0] if re.search(f'\\b{x.lower()}\\b', title.lower())]) * 2
                                    else:
                                        similarity = len([x for x in unit_groups[unit_group][1] if re.search(f'\\b{x.lower()}\\b', title.lower())])
                                    similarity /= len([x for x in unit_groups[unit_group][2] if re.search(f'\\b{x.lower()}\\b', title.lower())]) + 1
                                    if similarity > highest[0]:
                                        highest = (similarity, (major, sub_major, minor, unit_group))
                    isco08_major = highest[1][0]
                    isco08_submajor = highest[1][1]
                    isco08_minor = highest[1][2]
                    isco08_unit_group = highest[1][3]
            
        title = title.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:500]
        return title, title_custom, isco08_major, isco08_submajor, isco08_minor, isco08_unit_group


    def __parse_company_name(self, company_name):
        if company_name:
            return company_name.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:500]
        else:
            return 'nocompanyname'

    # Returns location according to the jobboard and a unified version
    def __parse_location(self, location_jobboard, title_jobboard, simple_parsing=False):
        try:
            location_unified_a = None
            location_unified_b = None
            location_jobboard = location_jobboard.replace('+', '').replace('*', '').strip()
            if location_jobboard and self.jobboard_country.lower() in self.locations:
                for city, city_details in self.locations[self.jobboard_country.lower()].items():
                    if city.lower() == location_jobboard.lower().strip():
                        location_unified_a = city
                        location_unified_b = city_details['adm_entity']
                        break
                if location_unified_a:
                    return location_jobboard, location_unified_a, location_unified_b
                if not simple_parsing:
                    for city, city_details in self.locations[self.jobboard_country.lower()].items():
                        if city_details['other_names_flashtext'].extract_keywords(location_jobboard.lower()) or city_details['name_flashtext'].extract_keywords(location_jobboard.lower()):
                        # if re.search(f"\\b{city.lower()}\\b", location_jobboard.lower()) or any([re.search(f"\\b{x.lower()}\\b", location_jobboard.lower()) for x in city_details['other_names']]):
                            location_unified_a = city
                            location_unified_b = city_details['adm_entity']
                            break
                    if location_unified_a:
                        return location_jobboard, location_unified_a, location_unified_b
                    for city, city_details in self.locations[self.jobboard_country.lower()].items():
                        if city_details['other_names_flashtext'].extract_keywords(title_jobboard.lower()) or city_details['name_flashtext'].extract_keywords(title_jobboard.lower()):
                        # if re.search(f"\\b{city.lower()}\\b", title_jobboard.lower()) or any([re.search(f"\\b{x.lower()}\\b", title_jobboard.lower()) for x in city_details['other_names']]):
                            location_unified_a = city
                            location_unified_b = city_details['adm_entity']
                            break
                    if location_unified_a:
                        return location_jobboard, location_unified_a, location_unified_b
                    for city, city_details in self.locations[self.jobboard_country.lower()].items():
                        if city_details['zip_codes_flashtext'].extract_keywords(location_jobboard.lower()):
                        # if any(re.search(f"\\b{x}\\b", location_jobboard) for x in city_details['zip_codes']):
                            location_unified_a = city
                            location_unified_b = city_details['adm_entity']
                            break
                    if location_unified_a:
                        return location_jobboard, location_unified_a, location_unified_b
                    for city, city_details in self.locations[self.jobboard_country.lower()].items():
                        if city_details['neighbourhoods_flashtext'].extract_keywords(location_jobboard.lower()):
                        # if any(re.search(f"\\b{x.lower()}\\b", location_jobboard.lower()) for x in city_details['neighbourhoods']):
                            location_unified_a = city
                            location_unified_b = city_details['adm_entity']
                            break
                    if location_unified_a:
                        return location_jobboard, location_unified_a, location_unified_b
                    # for city, city_details in self.locations[self.jobboard_country.lower()].items():
                    #     if SequenceMatcher(None, unidecode(city.lower()), unidecode(location_jobboard.lower().strip())).ratio() > 0.9:
                    #         location_unified_a = city
                    #         location_unified_b = city_details['adm_entity']
                    #         break
                    # if location_unified_a:
                    #     return location_jobboard, location_unified_a, location_unified_b
        except:
            print(traceback.format_exc())
        location_jobboard = location_jobboard.replace('"', '').replace("'", '').replace('’', '').replace('`', '').replace('\t', ' ').replace('\n', ' ').replace('  ', ' ').strip()[:500]
        if not location_unified_a:
            pass # Google API here
        return location_jobboard, location_unified_a, location_unified_b
                   
    # dodane przeze mnie do update'u
    # def __parse_update_date(self, update):
    #     if re.search('hours', update):
    #         update = datetime.today()
    #     else:
    #         update = None
    #     return update
    # def __parse_update_date(self, update):
    #     today = ['today', 'heute', 'dzis', 'min', 'hour', 'uur', 'vandaag', 'zojuist', 'gerade', 'recently', 'just', 'now', 'oggi', 'appena', 'stunde', 'uren', 'jetzt', 'juste', 'ahora', 'ora', 'ore', 'hoy', 'aujourd', 'heur', 'h fa', 'i dag', 'nettop', 'jour', 'instant', 'chwila', 'nyligen', 'idag', 'paiva', 'tanaan']
    #     yesterday = ['yesterday', 'gisteren', 'gestern', 'wczoraj', 'hier', 'i gar', 'ayer']
    #     day = ['day', 'tag', 'dzien', 'dni', 'dag', 'dia', 'journee', 'giorn']
    #     week = ['week', 'woche', 'semaine', 'seman', 'vecka', 'tydzien']
    #     month = ['month', 'monat', 'miesiac', 'miesiecy', 'mes', 'mois', 'maand', 'manad']
    #     hour = ['hour', 'hours', 'stunde', 'stunden']
    #     months = {'january':['gennaio', 'janvier', 'januar', 'januari'],
    #                 'february':['febbraio', 'février', 'februar', 'februari'],
    #                 'march':['marzo', 'mars', 'märz', 'mars'],
    #                 'april':['aprile', 'avril'],
    #                 'may':['maggio', 'mai', 'maj'],
    #                 'june':['giugno', 'juin', 'juni'],
    #                 'july':['luglio', 'juillet', 'juli'],
    #                 'august':['agosto', 'aout', 'augusti'],
    #                 'september':['settembre', 'septembre'],
    #                 'october':['ottombre', 'octobre', 'oktober'],
    #                 'november':['novembre', 'novembre'],
    #                 'december':['dicembre', 'décembre', 'dezember']}
    #     if type(update) is date:
    #         return update, update.day, update.month, update.year
    #     update = unidecode(update.strip())

    #     if any([d in update.lower() for d in today]):
    #         update = datetime.now().date()
    #     elif any([y in update.lower() for y in yesterday]):
    #         update = datetime.now().date() - timedelta(days=1)
    #     elif re.search(r'[0-9]{1,2}', update):
    #         update = re.search(r'[0-9]{1,2}', update).group()
    #         update_day = re.search(r'[0-9]{1,2}', update).group()
    #         if len(update_day) == 1:
    #             update_day = '0' + update_day
    #         update_month = re.search(r'[A-Za-z]{3,12}', update).group()
    #         update_year = re.search(r'20[0-9]{2}', update).group()
    #         for me, mi in months.items():
    #             if me in update_month.lower() or me[:3] in update_month.lower():
    #                 update = datetime.strptime(f'{update_day}-{me[:3].title()}-{update_year}', '%d-%b-%Y').date()
    #                 break
    #         else:
    #             for me, mi in months.items():
    #                 for m in mi:
    #                     if m in update_month.lower() or m[:3] in update_month.lower():
    #                         update = datetime.strptime(f'{update_day}-{me[:3].title()}-{update_year}', '%d-%b-%Y').date()
    #                         break
    #                 if type(update) == date:
    #                     break
    #     elif any([re.search(f"\\b{m}\\b", update.lower()) for m in list(months.keys()) + list(chain.from_iterable(months.values()))]) and re.search(r'\d+', update):
    #         if len(re.search(r'\d+', update).group()) == 1 or len(re.search(r'\d+', update).group()) == 2:
    #             day_of_month = re.search(r'\d+', update).group()
    #             if len(day_of_month) == 1:
    #                 day_of_month = '0' + day_of_month
    #             for me, mil in months.items():
    #                 if me in update.lower():
    #                     update = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
    #                     break
    #             else:
    #                 for me, mil in months.items():
    #                     for mi in mil:
    #                         if mi in update.lower():
    #                             update = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
    #                             break
    #                     if type(update) == date:
    #                         break
    #     elif any([re.search(f"\\b{m[:3]}", update.lower()) for m in list(months.keys()) + list(chain.from_iterable(months.values()))]) and re.search(r'\d+', update):
    #         if len(re.search(r'\d+', update).group()) == 1 or len(re.search(r'\d+', update).group()) == 2:
    #             day_of_month = re.search(r'\d+', update).group()
    #             if len(day_of_month) == 1:
    #                 day_of_month = '0' + day_of_month
    #             for me, mil in months.items():
    #                 if me[:3] in update.lower():
    #                     update = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
    #                     break
    #             else:
    #                 for me, mil in months.items():
    #                     for mi in mil:
    #                         if mi[:3] in update.lower():
    #                             update = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
    #                             break
    #                     if type(update) == date:
    #                         break
    #     elif any([d in update.lower() for d in day]) and re.search(r'\d+', update):
    #         days_ago = int(re.search(r'\d+', update).group())
    #         update = datetime.now().date() - timedelta(days=days_ago)
    #     elif re.search(" [1-5]*[0-9]{1}[h|m]", update.lower()):
    #         update = datetime.now().date()
    #     elif re.search(" [1-5]*[0-9]{1}d", update.lower()):
    #         update = datetime.now().date() - timedelta(days=int(re.search('[0-9]+', re.search(" [1-5]*[0-9]{1}d", update.lower()).group()).group()))
    #     elif any([w in update.lower() for w in week]) and re.search(r'\d+', update):
    #         weeks_ago = int(re.search(r'\d+', update).group())
    #         update = datetime.now().date() - timedelta(weeks=weeks_ago)
    #     elif any([w in update.lower() for w in week]):
    #         update = datetime.now().date() - timedelta(days=7)
    #     elif any([m in update.lower() for m in month]):
    #         return None, None, None, None
    #     else:
    #         print('\n --- Posting date not recognized: "' + str(update) + '" --- \n')
    #         return None, None, None, None
    #     if update > datetime.now().date():
    #         return None, None, None, None
    #     return update, update.day, update.month, update.year


    # Returns posting date as date object and day, month and year as integers
    def __parse_posting_date(self, posting_date):
        today = ['today', 'heute', 'dzis', 'min', 'hour', 'uur', 'vandaag', 'zojuist', 'gerade', 'recently', 'just', 'now', 'oggi', 'appena', 'stunde', 'uren', 'jetzt', 'juste', 'ahora', 'ora', 'ore', 'hoy', 'aujourd', 'heur', 'h fa', 'i dag', 'nettop', 'jour', 'instant', 'chwila', 'nyligen', 'idag', 'paiva', 'tanaan']
        yesterday = ['yesterday', 'gisteren', 'gestern', 'wczoraj', 'hier', 'i gar', 'ayer']
        day = ['day', 'tag', 'dzien', 'dni', 'dag', 'dia', 'journee', 'giorn']
        week = ['week', 'woche', 'semaine', 'seman', 'vecka', 'tydzien']
        month = ['month', 'monat', 'miesiac', 'miesiecy', 'mes', 'mois', 'maand', 'manad']
        months = {'january':['gennaio', 'janvier', 'januar', 'januari'],
                    'february':['febbraio', 'février', 'februar', 'februari'],
                    'march':['marzo', 'mars', 'märz', 'mars'],
                    'april':['aprile', 'avril'],
                    'may':['maggio', 'mai', 'maj'],
                    'june':['giugno', 'juin', 'juni'],
                    'july':['luglio', 'juillet', 'juli'],
                    'august':['agosto', 'aout', 'augusti'],
                    'september':['settembre', 'septembre'],
                    'october':['ottombre', 'octobre', 'oktober'],
                    'november':['novembre', 'novembre'],
                    'december':['dicembre', 'décembre', 'dezember']}
        if type(posting_date) is date:
            return posting_date, posting_date.day, posting_date.month, posting_date.year
        posting_date = unidecode(posting_date.strip())
        if re.search('[0-3][0-9]/[0-1][0-9]/20[1-9][0-9]', posting_date):
            posting_date = re.search('[0-3][0-9]/[0-1][0-9]/20[1-9][0-9]', posting_date).group()
            posting_date = datetime.strptime(posting_date, '%d/%m/%Y').date()
        elif re.search('20[1-9][0-9]/[0-1][0-9]/[0-3][0-9]', posting_date):
            posting_date = re.search('20[1-9][0-9]/[0-1][0-9]/[0-3][0-9]', posting_date).group()
            posting_date = datetime.strptime(posting_date, '%Y/%m/%d').date()
        elif re.search('[0-3][0-9]-[0-1][0-9]-20[1-9][0-9]', posting_date):
            posting_date = re.search('[0-3][0-9]-[0-1][0-9]-20[1-9][0-9]', posting_date).group()
            posting_date = datetime.strptime(posting_date, '%d-%m-%Y').date()
        elif re.search('20[1-9][0-9]-[0-1][0-9]-[0-3][0-9]', posting_date):
            posting_date = re.search('20[1-9][0-9]-[0-1][0-9]-[0-3][0-9]', posting_date).group()
            posting_date = datetime.strptime(posting_date, '%Y-%m-%d').date()
        elif re.search(r'[0-3][0-9]\.[0-1][0-9]\.20[1-9][0-9]', posting_date):
            posting_date = re.search(r'[0-3][0-9]\.[0-1][0-9]\.20[1-9][0-9]', posting_date).group()
            posting_date = datetime.strptime(posting_date, '%d.%m.%Y').date()
        elif re.search(r'[0-3]*[0-9]\.[0-1]*[0-9]', posting_date):
            posting_date = re.search(r'[0-3]*[0-9]\.[0-1]*[0-9]', posting_date).group()
            posting_date = datetime.strptime(posting_date, '%d.%m').date().replace(year=datetime.now().date().year)
        elif any([d in posting_date.lower() for d in today]):
            posting_date = datetime.now().date()
        elif any([y in posting_date.lower() for y in yesterday]):
            posting_date = datetime.now().date() - timedelta(days=1)
        elif re.search(r'[0-9]{1,2}.{1,2}[A-Za-z]{3,12}.{1,2}20[0-9]{2}', posting_date):
            posting_date = re.search(r'[0-9]{1,2}.{1,2}[A-Za-z]{3,12}.{1,2}20[0-9]{2}', posting_date).group()
            posting_date_day = re.search(r'[0-9]{1,2}', posting_date).group()
            if len(posting_date_day) == 1:
                posting_date_day = '0' + posting_date_day
            posting_date_month = re.search(r'[A-Za-z]{3,12}', posting_date).group()
            posting_date_year = re.search(r'20[0-9]{2}', posting_date).group()
            for me, mi in months.items():
                if me in posting_date_month.lower() or me[:3] in posting_date_month.lower():
                    posting_date = datetime.strptime(f'{posting_date_day}-{me[:3].title()}-{posting_date_year}', '%d-%b-%Y').date()
                    break
            else:
                for me, mi in months.items():
                    for m in mi:
                        if m in posting_date_month.lower() or m[:3] in posting_date_month.lower():
                            posting_date = datetime.strptime(f'{posting_date_day}-{me[:3].title()}-{posting_date_year}', '%d-%b-%Y').date()
                            break
                    if type(posting_date) == date:
                        break
        elif any([re.search(f"\\b{m}\\b", posting_date.lower()) for m in list(months.keys()) + list(chain.from_iterable(months.values()))]) and re.search(r'\d+', posting_date):
            if len(re.search(r'\d+', posting_date).group()) == 1 or len(re.search(r'\d+', posting_date).group()) == 2:
                day_of_month = re.search(r'\d+', posting_date).group()
                if len(day_of_month) == 1:
                    day_of_month = '0' + day_of_month
                for me, mil in months.items():
                    if me in posting_date.lower():
                        posting_date = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
                        break
                else:
                    for me, mil in months.items():
                        for mi in mil:
                            if mi in posting_date.lower():
                                posting_date = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
                                break
                        if type(posting_date) == date:
                            break
        elif any([re.search(f"\\b{m[:3]}", posting_date.lower()) for m in list(months.keys()) + list(chain.from_iterable(months.values()))]) and re.search(r'\d+', posting_date):
            if len(re.search(r'\d+', posting_date).group()) == 1 or len(re.search(r'\d+', posting_date).group()) == 2:
                day_of_month = re.search(r'\d+', posting_date).group()
                if len(day_of_month) == 1:
                    day_of_month = '0' + day_of_month
                for me, mil in months.items():
                    if me[:3] in posting_date.lower():
                        posting_date = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
                        break
                else:
                    for me, mil in months.items():
                        for mi in mil:
                            if mi[:3] in posting_date.lower():
                                posting_date = datetime.strptime(f'{day_of_month} {me[:3].title()}', '%d %b').replace(year=datetime.now().date().year).date()
                                break
                        if type(posting_date) == date:
                            break
        elif any([d in posting_date.lower() for d in day]) and re.search(r'\d+', posting_date):
            days_ago = int(re.search(r'\d+', posting_date).group())
            posting_date = datetime.now().date() - timedelta(days=days_ago)
        elif re.search(" [1-5]*[0-9]{1}[h|m]", posting_date.lower()):
            posting_date = datetime.now().date()
        elif re.search(" [1-5]*[0-9]{1}d", posting_date.lower()):
            posting_date = datetime.now().date() - timedelta(days=int(re.search('[0-9]+', re.search(" [1-5]*[0-9]{1}d", posting_date.lower()).group()).group()))
        elif any([w in posting_date.lower() for w in week]) and re.search(r'\d+', posting_date):
            weeks_ago = int(re.search(r'\d+', posting_date).group())
            posting_date = datetime.now().date() - timedelta(weeks=weeks_ago)
        elif any([w in posting_date.lower() for w in week]):
            posting_date = datetime.now().date() - timedelta(days=7)
        elif any([m in posting_date.lower() for m in month]):
            return None, None, None, None
        else:
            print('\n --- Posting date not recognized: "' + str(posting_date) + '" --- \n')
            return None, None, None, None
        if posting_date > datetime.now().date():
            return None, None, None, None
        return posting_date, posting_date.day, posting_date.month, posting_date.year


    def __shave_company_name(self, company_name):
        company_shaved_a = unidecode(company_name.replace(' AG', '').replace(' a ', '').replace(' now ', '').lower().replace('&co', '').replace('"', '').replace("'", '').replace('’', '').replace('s.a.', '').replace('`', '').replace('co.', '').replace('n.v.', '').replace('s.p.a.', '').replace('gmbh', '').replace(' corp', '').replace('.', '').replace(' group', '').replace(' llc', '').replace('incorporated', '').replace(' inc', '').replace(' plc', '').replace(' ltda', '').replace(' ltd', '').replace(' srl', '').replace('llp', '').replace('s/a', '').replace('company', '').replace('corporation', '').replace('world headquarters', '').replace('part of', '').replace('formerly ', '').replace('known as ', '').replace('a division of ', '').replace('international', '').replace('&', "and"). replace('+', 'and').replace('®', ''))
        company_shaved_b = [x.replace(')', '').replace('-', '').strip().replace(' ', '') for x in list(chain.from_iterable([a.split(' - ') for a in re.split("[|,(//•*]", company_shaved_a)])) if len(x.replace(')', '').replace('-', '').strip()) > 2]
        return company_shaved_b


    def __has_competitor_keyword(self, company):
        if any(x in company.lower() for x in ['personalservice', ' rpo ', 'staffing', 'personaldienstleistung', 'employment', 'recruitment', 'recruiting', 'recruiters', 'personnel', 'personalvermittlung']):
            return True
        return False

    def __parse_sector(self, company, advanced_sector_parsing=True):
        sector_custom = None
        gics_sector = None
        gics_industry_group = None
        gics_industry = None
        gics_sub_industry = None
        competition = False
        company = company.strip()
        company_shaved = self.__shave_company_name(company)
        company_name_unified = None
        if self.__has_competitor_keyword(company):
            competition = True
        if company in self.companies_sectors_linkedin:
            company_name_unified = company
            for gics_s, linkedin_s in self.linkedin_gics_dict.items():
                if self.companies_sectors_linkedin[company][1] in linkedin_s:
                    gics_sector = gics_s
                    if 'Staffing & Recruiting' == self.companies_sectors_linkedin[company][1]:
                        competition = True
                    return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified
        for c, s in self.companies_sectors_linkedin.items():
            if len(company) > 3 and unidecode(company.lower()) == unidecode(c.lower()):
                company_name_unified = c
                for gics_s, linkedin_s in self.linkedin_gics_dict.items():
                    if s in linkedin_s:
                        gics_sector = gics_s
                        if 'Staffing & Recruiting' == self.companies_sectors_linkedin[c][1]:
                            competition = True
                        return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified
        for c, s in self.companies_sectors_linkedin.items():
            if s[0].split(';')[0] == company_shaved[0]:
                company_name_unified = c
                for gics_s, linkedin_s in self.linkedin_gics_dict.items():
                    if s in linkedin_s:
                        gics_sector = gics_s
                        if 'Staffing & Recruiting' == self.companies_sectors_linkedin[c][1]:
                            competition = True
                        return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified
        for c, s in self.companies_sectors_linkedin.items():
            if any(x == y for y in s[0].split(';') for x in company_shaved):
                company_name_unified = c
                for gics_s, linkedin_s in self.linkedin_gics_dict.items():
                    if s in linkedin_s:
                        gics_sector = gics_s
                        if 'Staffing & Recruiting' == self.companies_sectors_linkedin[c][1]:
                            competition = True
                        return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified
        if company.lower() in self.companies_sectors:
            gics_sector = self.companies_sectors[company.lower()][0]
            if not competition:
                competition = self.companies_sectors[company.lower()][1]
            company_name_unified = self.companies_sectors[company.lower()][2]
            return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified
        if advanced_sector_parsing:
            for c, s in self.companies_sectors_linkedin.items():
                if any(SequenceMatcher(None, x, y).ratio() > 0.9 for x in s[0].split(';') for y in company_shaved if len(x) > 7):
                    company_name_unified = c
                    for gics_s, linkedin_s in self.linkedin_gics_dict.items():
                        if s in linkedin_s:
                            gics_sector = gics_s
                            self.companies_sectors[company.lower()] = [gics_sector, competition, company_name_unified]
                            with open('companies_sectors_map.json', 'w', encoding='utf8') as companies_sectors_f:
                                json.dump(self.companies_sectors, companies_sectors_f)
                            if 'Staffing & Recruiting' == self.companies_sectors_linkedin[c][1]:
                                competition = True
                            return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
                session = requests.Session()
                response = session.get(f"https://www.glassdoor.com/Reviews/company-reviews.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={company.strip().replace(' ', '-')}&sc.keyword={company.strip().replace(' ', '-')}&locT=&locId=&jobType=", headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                if soup.find('div', id='SearchSuggestions'):
                    company_shortened = ' '.join(company.split(' ')[:2])
                    response = session.get(f"https://www.glassdoor.com/Reviews/company-reviews.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={company_shortened.strip().replace(' ', '-')}&sc.keyword={company_shortened.strip().replace(' ', '-')}&locT=&locId=&jobType=", headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                if soup.find(class_='single-company-result module'):
                    link = 'https://www.glassdoor.com' + soup.find_all(class_='single-company-result module')[0].find('a').get('href')
                    time.sleep(1.5)
                    company_page_response = session.get(link, headers=headers)
                    company_page_soup = BeautifulSoup(company_page_response.content, 'html.parser')
                else:
                    company_page_soup = soup
                basic_info = company_page_soup.find('div', id='EmpBasicInfo')
                company_name_unified = basic_info.find('h2', class_='cell middle tightVert blockMob').text.replace(' Overview', '').strip()
                for entity in basic_info.find_all('div', class_='infoEntity'):
                    if 'Industry' in entity.text:
                        for gics, glassdoor in self.glassdoor_gics_dict.items():
                            for g in glassdoor:
                                if g == entity.text.replace('Industry', '').strip():
                                    if g == 'Staffing & Outsourcing':
                                        competition = True
                                    gics_sector = gics
            except:
                pass
            self.companies_sectors[company.lower()] = [gics_sector, competition, company_name_unified]
            with open('companies_sectors_map.json', 'w', encoding='utf8') as companies_sectors_f:
                json.dump(self.companies_sectors, companies_sectors_f)
        return sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competition, company_name_unified


    # Returns false if salary if for sure wrong, else true
    def __is_salary_plausible(self, employment_type, salary_in_eur_per_hour_max, intern_excluded=True):
        if employment_type:
            if 'parttime' in employment_type.replace('-','').replace(' ','').lower() and 'fulltime' not in employment_type.replace('-','').replace(' ','').lower():
                return False
        if salary_in_eur_per_hour_max < 1:
            return False
        if salary_in_eur_per_hour_max:
            if self.jobboard_country == 'Germany':
                if intern_excluded:
                    if salary_in_eur_per_hour_max < 9 and salary_in_eur_per_hour_max > 160:
                        return False
                else:
                    if salary_in_eur_per_hour_max < 2.8:
                        return False
            elif self.jobboard_country == 'United Kingdom':
                if intern_excluded:
                    if salary_in_eur_per_hour_max < 7 and salary_in_eur_per_hour_max > 180:
                        return False
                else:
                    if salary_in_eur_per_hour_max < 4:
                        return False
        return True


    def __find_max_and_min(self, salary):
        salary_max = None
        salary_min = None
        if re.search(r'\d', salary):
            if any([c == self.salary_currency for c in ['GBP', 'CHF', 'USD', 'JPY', 'AUD', 'CNY', 'INR']]):
                try:
                    salary_max = max(float(re.findall(r"\d+[,.']*\d+", salary)[0].replace(',','').replace("'",'')), float(re.findall(r"\d+[,.']*\d+", salary)[1].replace(',','').replace("'",'')))
                    if salary_max <= 2 * min(float(re.findall(r"\d+[,.']*\d+", salary)[0].replace(',','').replace("'",'')), float(re.findall(r"\d+[,.']*\d+", salary)[1].replace(',','').replace("'",''))):
                        salary_min = min(float(re.findall(r"\d+[,.']*\d+", salary)[0].replace(',','').replace("'",'')), float(re.findall(r"\d+[,.']*\d+", salary)[1].replace(',','').replace("'",'')))
                except:
                    salary_max = float(re.search(r"\d+[,.']*\d+", salary).group().replace(',','').replace("'",''))
            else:
                try:
                    salary_max = max(float(re.findall(r"\d+[,.']*\d+", salary)[0].replace('.','').replace(',','.')), float(re.findall(r"\d+[,.']*\d+", salary)[1].replace('.','').replace(',','.')))
                    if salary_max <= 2 * min(float(re.findall(r"\d+[,.']*\d+", salary)[0].replace('.','').replace(',','.')), float(re.findall(r"\d+[,.']*\d+", salary)[1].replace('.','').replace(',','.'))):
                        salary_min = min(float(re.findall(r"\d+[,.']*\d+", salary)[0].replace('.','').replace(',','.')), float(re.findall(r"\d+[,.']*\d+", salary)[1].replace('.','').replace(',','.')))
                except:
                    salary_max = float(re.search(r"\d+[,.']*\d+", salary).group().replace('.','').replace(',','.'))
        return salary_max, salary_min


    def __search_salary_in_description(self, full_description):
        for c in [self.salary_currency, '€', '£']:
            if c in full_description:
                sal_pos = full_description.index(c)
                salary_text_chunk = (full_description[sal_pos-35:sal_pos+35])
                if any([x in salary_text_chunk for x in self.year + self.month + self.week + self.day + self.hour]) and re.search(r'\d+', salary_text_chunk) and any([sw in salary_text_chunk.lower() for sw in self.salary_words]):
                    return salary_text_chunk
        return None


    def __salary_per_hr_and_timeframe(self, salary, salary_max, salary_min, hours_per_year, hours_per_month, hours_per_week, hours_per_day):
        salary_timeframe = None
        salary_in_eur_per_hour_max = None
        salary_in_eur_per_hour_min = None
        if any([t in unidecode(salary.lower()) for t in self.year]):
            salary_timeframe = 'year'
            salary_in_eur_per_hour_max = salary_max / self.currency_rate / hours_per_year
            if salary_min:
                salary_in_eur_per_hour_min = salary_min / self.currency_rate / hours_per_year
        elif any([t in unidecode(salary.lower()) for t in self.month]):
            salary_timeframe = 'month'
            salary_in_eur_per_hour_max = salary_max / self.currency_rate / hours_per_month
            if salary_min:
                salary_in_eur_per_hour_min = salary_min / self.currency_rate / hours_per_month
        elif any([t in unidecode(salary.lower()) for t in self.week]):
            salary_timeframe = 'week'
            salary_in_eur_per_hour_max = salary_max / self.currency_rate / hours_per_week
            if salary_min:
                salary_in_eur_per_hour_min = salary_min / self.currency_rate / hours_per_week
        elif any([t in unidecode(salary.lower()) for t in self.day]):
            salary_timeframe = 'day'
            salary_in_eur_per_hour_max = salary_max / self.currency_rate / hours_per_day
            if salary_min:
                salary_in_eur_per_hour_min = salary_min / self.currency_rate / hours_per_day
        elif any([t in unidecode(salary.lower()) for t in self.hour]):
            salary_timeframe = 'hour'
            salary_in_eur_per_hour_max = salary_max / self.currency_rate
            if salary_min:
                salary_in_eur_per_hour_min = salary_min / self.currency_rate
        return salary_timeframe, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min


    def __parse_salary(self, salary, employment_type, full_description, link, hours_per_year=2080, hours_per_month=170, hours_per_week=40, hours_per_day=8):
        if salary:
            salary = salary.strip()
        elif self.__search_salary_in_description(full_description):
            salary = self.__search_salary_in_description(full_description)
        else:
            return None, None, None, None, None
 
        salary_max, salary_min = self.__find_max_and_min(salary)
        salary_timeframe, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min = self.__salary_per_hr_and_timeframe(salary, salary_max, salary_min, hours_per_year, hours_per_month, hours_per_week, hours_per_day)
 
        if salary_in_eur_per_hour_max:
            if self.__is_salary_plausible(employment_type, salary_in_eur_per_hour_max):
                return salary_max, salary_min, salary_timeframe, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min
        else:
            return None, None, None, None, None


    def __parse_agency_or_direct(self, agency_or_direct):
        if agency_or_direct:
            agency_or_direct = agency_or_direct.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:100]
        return agency_or_direct


    def __parse_employment_type(self, employment_type):
        if employment_type:
            employment_type = employment_type.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:200]
        return employment_type


    def __parse_full_description(self, full_description):
        if full_description:
            full_description = full_description.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:4000]
        return full_description

    def __parse_skills(self, skills, full_description, advanced_skill_search):
        if skills:
            skills = skills.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:4000]
        else:
            skills = ''
            if advanced_skill_search:
                list_of_words =  full_description.split(' ')
                for skill in self.skills_list:
                    if len(skill.split(' ')) == 4:
                        for num, word in enumerate(list_of_words[:-3]):
                            current_phrase = f'{word} {list_of_words[num+1]} {list_of_words[num+2]} {list_of_words[num+3]}'
                            if SequenceMatcher(None, current_phrase.lower(), skill.lower()).ratio() > 0.8:
                                skills += (';' + skill)
                    elif len(skill.split(' ')) == 3:
                        for num, word in enumerate(list_of_words[:-2]):
                            current_phrase = f'{word} {list_of_words[num+1]} {list_of_words[num+2]}'
                            if SequenceMatcher(None, current_phrase.lower(), skill.lower()).ratio() > 0.85:
                                skills += (';' + skill)
                    elif len(skill.split(' ')) == 2:
                        for num, word in enumerate(list_of_words[:-1]):
                            current_phrase = f'{word} {list_of_words[num+1]}'
                            if SequenceMatcher(None, current_phrase.lower(), skill.lower()).ratio() > 0.9:
                                skills += (';' + skill)
                    if len(skill.split(' ')) == 1:
                        if len(skill) <= 4:
                            if re.search(f'\\b{word}\\b', skill):
                                skills += (';' + skill)
                        else:
                            if SequenceMatcher(None, word.lower(), skill.lower()).ratio() > 0.9:
                                skills += (';' + skill)
            else:
                skills = ';'.join(list(set(self.skills_keyword_processor_short.extract_keywords(unidecode(full_description.replace('i.d.R.', ''))))) + list(set(self.skills_keyword_processor_long.extract_keywords(full_description))))
            skills = skills[:4000]
            if len(skills) == 0:
                skills = None
        return skills


    def __parse_link(self, link):
        if link:
            link = link.replace('"', '').replace("'", '').replace('’', '').replace('`', '').strip()[:4000]
        return link


    def __get_id(self, title, company_name, location_jobboard, posting_date_day, posting_date_month, posting_date_year):
        return unidecode(((title + company_name + location_jobboard).replace(' ', '').replace('\n', '').replace('\t', '').replace('"', '').replace("'", '').replace('’', '').replace('`', '') + str(posting_date_day) + str(posting_date_month) + str(posting_date_year))[:800])


    ############# API #############


    def enter_log(self, mssg_type, mssg):
        if mssg_type.lower() == 'error':
            logging.error(mssg)
        elif mssg_type.lower() == 'info':
            logging.info(mssg)


    def get_full_desc(self, soup_page):
        text = soup_page.find_all(text=True)
        description = 'DESCRIPTION EXTRACTED FROM AN EXTERNAL PAGE\n'
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            'style'
        ]
        for t in text:
            if t.parent.name not in blacklist:
                description += '{} '.format(t)
        return description


    def map_sector(self, sector_input):
        sectors_map = {
            'Energy': ['Energie'],
            'Materials': ['Materialwirtschaft', 'Chemie', 'Metall'],
            'Industrials': ['Architektur und Bauwesen', 'Assistenz und Sekretariat', 'Fahrzeugbau und Zulieferer', 'Fertigung', 'Handwerk und gewerblich technische Berufe', 'Logistik', 'Projektmanagement', 'Sales und Vertrieb', 'Technische Berufe und Ingenieurwesen', 'Administration', 'Arbeit', 'Architektur', 'Aushilfe', 'Bau', 'Büro', 'Business', 'Consulting', 'Controlling', 'Design', 'Dienstleistung', 'Elektro', 'Fertigung', 'Handel', 'Handwerk', 'Ingenieurwesen', 'Kundendienst', 'Lager', 'Leitung', 'Logistik', 'Management', 'Naturwissenschaft', 'Office', 'Personalwesen', 'Praktikum', 'Produktion', 'Sales', 'Service', 'Sicherheit', 'Technik', 'Transport', 'Verkehr', 'Vertrieb', 'Wirtschaft'],
            'Consumer Discretionary': ['Tourismus', 'Automobil', 'Bildung', 'Gastronomie', 'Hotel', 'Customer Support', 'Kundenservice', 'Kunst', 'Recht', 'Restaurant', 'Verkauf'],
            'Consumer Staples': ['Landwirtschaft'],
            'Health Care': ['Gesundheitswesen', 'Geisteswissenschaft', 'Gesundheit', 'Pflege', 'Pharma', 'Wellness'],
            'Financials': ['Finanzen', 'Accounting', 'Analyse', 'Bank', 'Finance', 'Rechnungswesen', 'Steuern', 'Versicherung'],
            'Information Technology': ['Internet, Web und Softwareentwicklung', 'Computer', 'Developer', 'Internet', 'IT'],
            'Communication Services': ['Marketing, PR und Werbung', 'Marketing', 'Medien', 'Sprachen', 'Sport', 'Telekommunikation', 'Werbung'],
            'Utilities': [],
            'Real Estate': ['Immobilien'],
            'Government & Public Services': ['Militär', 'Verwaltung']
        }
        for sg, so in sectors_map.items():
            if any(x.lower() in sector_input.lower() for x in so):
                return sg
        return None


    # def printing(self, title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link, update, advanced_skill_search=False, check_if_exists=False):
    def printing(self, title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link, advanced_skill_search=False, check_if_exists=False):
    # def printing(self, title, company_name, location_jobboard = location_jobboard, posting_date = posting_date, sector_jobboard = sector_jobboard, salary = salary, agency_or_direct = agency_or_direct, employment_type = employment_type, full_description = full_description, skills = skills, link = link, advanced_skill_search=False, check_if_exists=False):
        try:
            title_jobboard, title_custom, isco08_major, isco08_submajor, isco08_minor, isco08_unit_group = self.__parse_title(title)
            company_name_jobboard = self.__parse_company_name(company_name)
            location_jobboard, location_unified_a, location_unified_b = self.__parse_location(location_jobboard, title_jobboard)
            posting_date, posting_date_day, posting_date_month, posting_date_year = self.__parse_posting_date(posting_date)
            sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, competitor, company_name_unified = self.__parse_sector(company_name_jobboard, advanced_sector_parsing=True)
            if not company_name_unified:
                company_name_unified = company_name_jobboard
            if gics_sector:
                sector_custom = gics_sector
            else:
                sector_custom = self.map_sector(sector_jobboard)
            salary_max, salary_min, salary_timeframe, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min = self.__parse_salary(salary, employment_type, full_description, link)
            # salary = self.__parse_salary(salary, employment_type, full_description, link)
            scraping_date = datetime.now().date()
            agency_or_direct = self.__parse_agency_or_direct(agency_or_direct)
            employment_type = self.__parse_employment_type(employment_type)
            full_description = self.__parse_full_description(full_description)
            skills = self.__parse_skills(skills, full_description, advanced_skill_search)
            link = self.__parse_link(link)
            # update = self.__parse_update_date(update)
            # id_str = self.__get_id(scraping_date, title, company_name_jobboard, location_jobboard, posting_date_day, posting_date_month, posting_date_year)
  
            # return scraping_date, title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link, update
            return scraping_date, title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link
            # if check_if_exists:
            #     # with pyodbc.connect('DRIVER='+self.db_config['driver']+';SERVER='+self.db_config['server']+';PORT=1433;DATABASE='+self.db_config['database']+';UID='+self.db_config['username']+';PWD='+self.db_config['password']) as cnxn:
            #     cursor = self.cnxn.cursor()
            #     cursor.execute(f"If EXISTS (SELECT id FROM jobboard_{self.jobboard_name.replace('.','_').replace('-', '_').lower()} WHERE id = '{id_str}') BEGIN SELECT 1 END ELSE BEGIN SELECT 0 END")
            #     if cursor.fetchone()[0] == 0:
            #         cursor.execute(f"INSERT INTO dbo.jobboard_{self.jobboard_name.replace('.','_').replace('-', '_').lower()}(id, scraping_date, jobboard_country, jobboard_name, title_jobboard, title_custom, competitor, isco08_major, isco08_submajor, isco08_minor, isco08_unit_group, company_name_jobboard, company_name_unified, location_jobboard, location_unified_a, location_unified_b, posting_date, posting_date_day, posting_date_month, posting_date_year, sector_jobboard, sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, salary_max, salary_min, salary_timeframe, salary_currency, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min, agency_or_direct, employment_type, full_description, skills, link, other) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", id_str, scraping_date, self.jobboard_country, self.jobboard_name, title_jobboard, title_custom, competitor, isco08_major, isco08_submajor, isco08_minor, isco08_unit_group, company_name_jobboard, company_name_unified, location_jobboard, location_unified_a, location_unified_b, posting_date, posting_date_day, posting_date_month, posting_date_year, sector_jobboard, sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, salary_max, salary_min, salary_timeframe, self.salary_currency, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min, agency_or_direct, employment_type, full_description, skills, link, other)
            #         self.cnxn.commit()
            #         print('Uploaded to DB\n')
            # else:
            #     # with pyodbc.connect('DRIVER='+self.db_config['driver']+';SERVER='+self.db_config['server']+';PORT=1433;DATABASE='+self.db_config['database']+';UID='+self.db_config['username']+';PWD='+self.db_config['password']) as cnxn:
            #     cursor = self.cnxn.cursor()
            #     cursor.execute(f"INSERT INTO dbo.jobboard_{self.jobboard_name.replace('.','_').replace('-', '_').lower()}(id, scraping_date, jobboard_country, jobboard_name, title_jobboard, title_custom, competitor, isco08_major, isco08_submajor, isco08_minor, isco08_unit_group, company_name_jobboard, company_name_unified, location_jobboard, location_unified_a, location_unified_b, posting_date, posting_date_day, posting_date_month, posting_date_year, sector_jobboard, sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, salary_max, salary_min, salary_timeframe, salary_currency, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min, agency_or_direct, employment_type, full_description, skills, link, other) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", id_str, scraping_date, self.jobboard_country, self.jobboard_name, title_jobboard, title_custom, competitor, isco08_major, isco08_submajor, isco08_minor, isco08_unit_group, company_name_jobboard, company_name_unified, location_jobboard, location_unified_a, location_unified_b, posting_date, posting_date_day, posting_date_month, posting_date_year, sector_jobboard, sector_custom, gics_sector, gics_industry_group, gics_industry, gics_sub_industry, salary_max, salary_min, salary_timeframe, self.salary_currency, salary_in_eur_per_hour_max, salary_in_eur_per_hour_min, agency_or_direct, employment_type, full_description, skills, link, other)
            #     self.cnxn.commit()
            #     print('Uploaded to DB\n')
        except:
            traceback.print_exc()


    def exists_in_db(self, title, company_name, posting_date, location_jobboard):
        title_jobboard, _, _, _, _, _ = self.__parse_title(title, simple_parsing=True)
        company_name_jobboard = self.__parse_company_name(company_name)
        location_jobboard, _, _ = self.__parse_location(location_jobboard, title_jobboard, simple_parsing=True)
        _, posting_date_day, posting_date_month, posting_date_year = self.__parse_posting_date(posting_date)
        id_str = self.__get_id(title_jobboard, company_name_jobboard, location_jobboard, posting_date_day, posting_date_month, posting_date_year)
        # with pyodbc.connect('DRIVER='+self.db_config['driver']+';SERVER='+self.db_config['server']+';PORT=1433;DATABASE='+self.db_config['database']+';UID='+self.db_config['username']+';PWD='+self.db_config['password']) as cnxn:
        # cursor = self.cnxn.cursor()
        # cursor.execute(f"If EXISTS (SELECT id FROM jobboard_{self.jobboard_name.replace('.','_').replace('-', '_').lower()} WHERE id = '{id_str}') BEGIN SELECT 1 END ELSE BEGIN SELECT 0 END")
        if cursor.fetchone()[0] == 0:
            return False
        else:
            print('Already in DB\n')
            return False


    # def send_email(self, subject, message):
    #     email = 'horacy.niew@gmail.com'
    #     password = 'sjf!2#abc'
    #     send_to_email = 'tobias.talaj@gmail.com'

    #     msg = MIMEMultipart()
    #     msg['From'] = email
    #     msg['To'] = send_to_email
    #     msg['Subject'] = subject

    #     # Attach the message to the MIMEMultipart object
    #     msg.attach(MIMEText(message, 'plain'))

    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    #     server.starttls()
    #     server.login(email, password)
    #     text = msg.as_string()
    #     server.sendmail(email, send_to_email, text)
    #     server.quit()


    # def close_db_cnxn(self):
    #     self.cnxn.close()
