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
import sys
import traceback
import datetime

def err(type, value, tb):
    print("Exception date time: {}".format(datetime.datetime.now()))
    print(traceback.print_tb(tb))
sys.excepthook = err

path = r'C:\Users\tobiasz\Desktop\VS Code\chromedriver.exe'
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
driver = webdriver.Chrome(executable_path=path, chrome_options=opts)
driver.maximize_window()
links = [ 
'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Berlin__2c-Berlin&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Hamburg__2c-Hamburg&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=München__2c-Bayern&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Köln__2c-Nordrhein__2dWestfalen&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Frankfurt-am-Main__2c-Hessen&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Stuttgart__2c-Baden__2dWürttemberg&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Hannover__2c-Niedersachsen&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Nürnberg__2c-Bayern&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Düsseldorf__2c-Nordrhein__2dWestfalen&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Essen__2c-Nordrhein__2dWestfalen&rad=2&tm=30',

'https://www.monster.de/jobs/suche/Festanstellung_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Freie-Mitarbeit-Dienstvertrag_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Praktikum_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Vollzeit_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Teilzeit_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Befristet_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Student_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Berufsausbildung_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
'https://www.monster.de/jobs/suche/Diplomarbeit_8?cy=de&intcid=swoop_HeroSearch&where=Dortmund__2c-Nordrhein__2dWestfalen&rad=2&tm=30',
]


total = []
total_offers = []
num = 7884
link_num = 71
# with open(r'C:\Users\danie\Desktop\Python\Praca\Countries\Germany\Jobboards\links.txt') as links:
for url in links[70:]:
    print(url)
    driver.get(url)
    try:
        driver.maximize_window()
    except:
        None
    time.sleep(3)
    # input()
    try:
        cookie = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div/div[2]/div/button[2]')
        cookie.click()
    except:
        None
    time.sleep(2)

    action = webdriver.ActionChains(driver)
    try:
        slider = driver.find_element_by_xpath('//*[@id="ResultsContainer"]/div[2]/div')
    except:
        try:
            time.sleep(2)
            slider = driver.find_element_by_xpath('//*[@id="ResultsContainer"]/div[2]/div')
        except:
            pass
    try:
        ActionChains(driver).drag_and_drop_by_offset(slider, 0, 240).perform()
    except:
        pass
    try:
        next_button = driver.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div/div[1]/div[2]/a[1]')
        next_button.click()
    except:
        # input()
        try:
            next_button = driver.find_element_by_xpath('/html/body/div[3]/main/div[1]/div[1]/div/div[1]/div[2]/a[1]')
            next_button.click()
        except:
            None
    strona = 1
    while True:
        time.sleep(3)
        # slider = driver.find_element_by_xpath('//*[@id="ResultsContainer"]/div[2]/div')
        try:
            ActionChains(driver).drag_and_drop_by_offset(slider, 0, 100).perform()
        except:
            time.sleep(3)
            try:
                ActionChains(driver).drag_and_drop_by_offset(slider, 0, 60).perform()
            except:
                try:
                    ActionChains(driver).drag_and_drop_by_offset(slider, 0, 40).perform()
                except:
                    ActionChains(driver).drag_and_drop_by_offset(slider, 0, 20).perform()
        # else:
        #     print('enter')
        #     input()
        try:
            try:
                next_button = driver.find_element_by_xpath('/html/body/div[2]/main/div[1]/div[1]/div/div[1]/div[2]/a[1]')
                next_button.click()
            except:
                next_button = driver.find_element_by_xpath('/html/body/div[3]/main/div[1]/div[1]/div/div[1]/div[2]/a[1]')
                next_button.click()
        except:
            break
        print('strona: ', strona)
        if strona == 20:
            break
        strona += 1
    table = driver.find_element_by_id('SearchResults')
    ads = table.find_elements_by_class_name('card-content')
    print(len(ads))


    for ad in ads:
        try:
            header = ad.find_element_by_class_name('title').find_element_by_tag_name('a')
        except:
            continue
        title = header.text.strip()
        link = header.get_attribute('href')
        company_name = ad.find_element_by_class_name('company').find_element_by_class_name('name').text.strip()
        location_jobboard = ad.find_element_by_class_name('location').find_element_by_class_name('name').text.strip()
        posting_date = ad.find_element_by_tag_name('time').text.strip()
         
        p = re.compile(r'[0-9]') 
        p = p.findall(posting_date)
        try:
            days = int(''.join(p))
            posting_date = date.today() - timedelta(days)
        except:
            posting_date = date.today()
            
        agency_or_direct = 'Monster_DE'
        
        # parsowanie oferty
        session = requests.Session()            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        try:
            response_obj = session.get(link, headers=headers)
        except:
            time.sleep(3)
            response_obj = session.get(link, headers=headers)
        soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

        try:
            right_box = soup_obj.find('div', class_= 'mux-job-summary')
            rows = right_box.find_all('dl', class_= 'header')
        except:
            right_box = None
            rows = None
        dict = {}
        try:
            for i in rows:
                k = i.find('dt', class_= 'key').text.strip()
                try:
                    v = i.find_all('dd', class_= 'value').text.strip()
                except:
                    v = i.find('dd', class_= 'value').text.strip()
                
                dict[k] = []
                dict[k].append(v)
        except:
            None
        
        try:
            employment_type = str(dict['Vertragsart']).replace('[', '').replace(']', '').replace("'", '')
        except:
            employment_type = None
        try:
            sector_jobboard = str(dict['Branchen']).replace('[', '').replace(']', '').replace("'", '')
        except:
            sector_jobboard = None
        try:
            salary = soup_obj.find('div', class_= 'col-xs-12 cell').text.replace('Gehaltsangaben', '').strip()
        except:
            salary = None
                
        try:
            full_description = soup_obj.find('span', id= 'TrackingJobBody').text.strip()
        except:
            try:
                full_description = soup_obj.find('div', class_='details-content').text.strip()
            except:
                try:
                    content = soup_obj.find('body').find_all('div', recursive=False)
                    for i in content:
                        try:
                            full_description += i.text
                        except:
                            None
                except:
                    full_description = None
        
        skills = None
        new = ((title, company_name, location_jobboard, posting_date, sector_jobboard, salary, agency_or_direct, employment_type, full_description, skills, link))
        total.append(new)
        time.sleep(1)
        print(num)
        num += 1

    for i in total:
        if i not in total_offers:
            total_offers.append(i)

    df = pd.DataFrame(total_offers, columns = ['Title', 'Company Name', 'Location', 'Date', 'Sector', 'Salary', 'Agency or Direct', 'Employment Type', 'Description', 'Skills', 'Link'])
    df.to_excel(f'Monster_DE_{str(link_num)}.xlsx')
    link_num += 1