from pickle import FALSE
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from pynput.keyboard import Key, Controller
from datetime import date
import traceback
import pyodbc
import time
import random
import re
import pyperclip
import json


db_config_path = r'path\db_config.json'
with open(db_config_path, 'r', encoding='utf8') as f:
    db_config = json.load(f)


def create_searchstring(driver):
    job_titles = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='jobTitle-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    locations = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='location-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    skills = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='skill-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    companies = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='company-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    try:
        graduation = driver.find_element_by_xpath("//li[@aria-labelledby='eduYears-label']").find_element_by_xpath(".//span[@class='pill-text']").text
    except:
        graduation = ''
    schools = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='school-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    industries = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='industry-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    try:
        keywords = driver.find_element_by_xpath("//li[@aria-labelledby='keywords-label']").find_element_by_xpath(".//span[@class='pill-text']").text
    except:
        keywords = ''
    employemt_type = [t.text for t in driver.find_element_by_xpath("//li[@aria-labelledby='employmentType-label']").find_elements_by_xpath(".//span[@class='pill-text']")]
    searchstring = f'Job titles: {"+".join(job_titles)}| Locations: {"+".join(locations)}| Skills: {"+".join(skills)}| Companies: {"+".join(companies)}| Year of Graduation: {graduation}| Schools: {"+".join(schools)}| Industries: {"+".join(industries)}| Keywords: {keywords}| Employment type: {"+".join(employemt_type)}'
    return searchstring

def upload_to_database(searchstring, scraping_date, profile_name, title_company_main, location_main, industry_main, school_main, summary, positions):
    while len(positions) < 4:
        positions.append([None,None,None,None,None,None])
    with pyodbc.connect('DRIVER='+db_config['driver']+';SERVER='+db_config['server']+';PORT=1433;DATABASE='+db_config['database']+';UID='+db_config['username']+';PWD='+db_config['password']) as cnxn:
        cursor = cnxn.cursor()
        cursor.execute(f"SELECT COUNT(1) FROM li_profiles_2020_2 WHERE profile_name = '{profile_name}' AND title_company_main = '{title_company_main}'")
        already_exists = cursor.fetchone()[0]
        if already_exists == 0:
            cursor.execute("INSERT INTO dbo.li_profiles_2020_2(searchstring, scraping_date, profile_name, title_company_main, location_main, industry_main, school_main, summary, position_0_title, position_0_company, position_0_daterange, position_0_duration_in_months, position_0_location, position_0_description, position_1_title, position_1_company, position_1_daterange, position_1_duration_in_months, position_1_location, position_1_description, position_2_title, position_2_company, position_2_daterange, position_2_duration_in_months, position_2_location, position_2_description, position_3_title, position_3_company, position_3_daterange, position_3_duration_in_months, position_3_location, position_3_description) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", searchstring, scraping_date, profile_name, title_company_main, location_main, industry_main, school_main, summary, positions[0][0], positions[0][1], positions[0][2], positions[0][3], positions[0][4], positions[0][5], positions[1][0], positions[1][1], positions[1][2], positions[1][3], positions[1][4], positions[1][5], positions[2][0], positions[2][1], positions[2][2], positions[2][3], positions[2][4], positions[2][5], positions[3][0], positions[3][1], positions[3][2], positions[3][3], positions[3][4], positions[3][5])
            cnxn.commit()


def next_profile_page(page_nr):
    try:
        if page_nr == 0:
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div[1]/div/ul/li/a/span[1]').click()
        else:
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div[1]/div/ul/li[2]/a/span[1]').click()
    except:
        input("Couldn't proceed")
        time.sleep(2)
        if page_nr == 0:
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div[1]/div/ul/li/a/span[1]').click()
        else:
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div[1]/div/ul/li[2]/a/span[1]').click()


driver = webdriver.Chrome(r'C:\Users\danie\Desktop\Python\Scrapers\LinkedIn\chromedriver.exe')
actions = ActionChains(driver)
keyboard = Controller()

# Opening LinkedIn
driver.get('https://www.linkedin.com/cap/dashboard/home?recruiterEntryPoint=true&trk=nav_account_sub_nav_cap')
time.sleep(2)

file_name = input('Press enter ')
for second in range(5, 0, -1):
    print(second)
    time.sleep(1)


driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cancel'])[1]/following::button[1]").click()
time.sleep(3)

searchstring = create_searchstring(driver)

ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
page_content = pyperclip.paste()

actions = ActionChains(driver)
actions.move_by_offset(-290 + random.randint(-1, 1), 128 + random.randint(-1, 1))
actions.perform()
time.sleep(1)
actions.click()
actions.perform()
time.sleep(random.random()+3)

talentpool = int(driver.find_element_by_xpath("//span[@class='stats']").text.replace('1 of ', '').replace(',',''))
time.sleep(random.random()+1) 


failed = 0
if talentpool > 999:
    talentpool = 999
for candidate_nr in range(talentpool-1):
    try:
        time.sleep(random.random()+4)
        name = driver.find_element_by_xpath("//h1[@class='searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        try:
            title_company_main = driver.find_element_by_xpath("//li[@class='title searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        except:
            title_company_main = None
        try:
            location_main = driver.find_element_by_xpath("//span[@class='location searchable']/a").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        except:
            location_main = None
        try:
            industry_main = driver.find_element_by_xpath("//span[@class='industry searchable']/a").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        except:
            industry_main = None
        try:
            school_main = driver.find_element_by_xpath("//div[@class='profile-info']/p").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        except:
            school_main = None
        try:
            summary = driver.find_element_by_xpath("//div[@class='module-body searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        except:
            summary = None
        positions = driver.find_element_by_xpath("//div[@id='profile-experience']").find_elements_by_xpath(".//li[@class='position']")
        last_position = driver.find_element_by_xpath("//div[@id='profile-experience']").find_element_by_xpath(".//li[@class='position last']")
        print(name)
        print(title_company_main)
        print('---')
        db_positions = []
        for position in positions[:-1]:
            title = position.find_element_by_xpath(".//h4[@class='searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
            company = position.find_element_by_xpath(".//h5[@class='searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
            daterange = position.find_element_by_xpath(".//p[@class='date-range']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
            try:
                duration = position.find_element_by_xpath(".//span[@class='duration']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
                daterange = daterange.replace(duration, '')
                if 'year' in duration:
                    duration = int(re.search(r'\d+', duration.split('year')[0]).group())*12 + int(re.search(r'\d+', duration.split('year')[1]).group())
                else:
                    duration = int(re.search(r'\d+', duration).group())
            except:
                duration = None
            try:
                location = position.find_element_by_xpath(".//span[@class='location']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
                daterange = daterange.replace(location, '')
            except:
                location = None
            try:
                description = position.find_element_by_xpath(".//p[@class='description searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
            except:
                description = None
            db_positions.append([title, company, daterange, duration, location, description])

        title = last_position.find_element_by_xpath(".//h4[@class='searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        company = last_position.find_element_by_xpath(".//h5[@class='searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        daterange = last_position.find_element_by_xpath(".//p[@class='date-range']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        try:
            duration = last_position.find_element_by_xpath(".//span[@class='duration']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
            daterange = daterange.replace(duration, '')
            if 'year' in duration:
                duration = int(re.search(r'\d+', duration.split('year')[0]).group())*12 + int(re.search(r'\d+', duration.split('year')[1]).group())
            else:
                duration = int(re.search(r'\d+', duration).group())
        except:
            duration = None
        try:
            location = last_position.find_element_by_xpath(".//span[@class='location']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
            daterange = daterange.replace(location, '')
        except:
            location = None
        try:
            description = last_position.find_element_by_xpath(".//p[@class='description searchable']").text.replace('"', '').replace("'", '').replace('’', '').replace('`', '')
        except:
            description = None
        db_positions.append([(title), company, daterange, duration, location, description])

        upload_to_database(searchstring, date.today(), name, title_company_main, location_main, industry_main, school_main, summary, db_positions)
    except:
        traceback.print_exc()
        failed += 1

    next_profile_page(candidate_nr)

print('Failed: ', failed)
