from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import functools
import datetime
import json
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
# warnings.filterwarnings("ignore", category=UserWarning)

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        
        start_time = time.perf_counter()

        try:
            value = func(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            end_hour = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"Finished {func.__name__!r} in {run_time:.4f} secs at {end_hour}. It took {time.strftime('%H:%M:%S', time.gmtime(run_time))}.")
            
            return value
        except (RuntimeError, TypeError, NameError, OSError, BaseException, ValueError) as err:
            end_time = time.perf_counter()
            run_time = end_time - start_time
            end_hour = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"\n\nATTENZIONE\n\n{func.__name__} failed after {run_time:.4f} secs at {end_hour}. It took {time.strftime('%H:%M:%S', time.gmtime(run_time))}.\n\nUnexpected {err=}, {type(err)=}\n\n")
            
    return wrapper_timer

@timer
def moodys_scraper_func(file_name):
    df = pd.read_excel(file_name)
    def yahoo_scraper_func():
        ticker_dict = {}
        counter_yahoo = 0
        bag_of_useless = ['Private', 'Foreign Owned', '-', 'n/a', 'Government', 'HSE.TO','GTES', ' ARD', 'Privately held by MMJ Group Holdings Limited (MMJJF), an Austrailian-listed company.', "Gov't", 'None', 'Non-Profit', '', 'Foreign Parent-9375.T ticker?', "State Gov't",  'GPS (The GAP)', 'Tribal Government', 'Bankruptcy', 'Private Equity', 'Private?', 'Non-profit organization', 'N/a', 'Sumitomo Mitsui Trust Holdings Inc.', '532540 (India: Bombay)', 'VLVLY (TICKER)  / VOLVY (MOODYS)', '2162 (JASDAQ)', 'RCRUY (parent)', 0, 'Province of Quebec', 'UTX', 'VLVY', 'Foreign Parent', 'Goverment', 'MIK', 'private', 'Foreign', 'RTIX/SRGA', 'SAMSNG', 'SEB SA', 'HSE', 'SIE', ' ', 'VSVS', 'VOLVY', 'BRK', '\\xa0', 'HINDALCO', 'Fed Owned', 'AEXAY (parent)', 'C ', 'NEMTF', 'CSGN', 'SDF', ' LH', 'NEOS', 'GAS', 'CVIA', 'FCAU', 'ETH', 'JASN', 'IEP (Parent)', 'PRSC', 'CLGX', '2162 (JASDAQ)', 'RCRUY (parent)']
        bag_of_empty = []

        for index, row in df.iterrows():
            ticker = row['Ticker'] 
            print('Row: ', index)       # doesn't have to be printed
            
            if ticker not in ticker_dict:
                if ticker not in bag_of_useless:
                    try:
                        ticker_dict[ticker] = index
                        counter_yahoo += 1

                        # parsing summary data
                        summary_link = "https://finance.yahoo.com/quote/{ticker}?p={ticker}".format(ticker=ticker)
                        
                        # BS4 inside an offer
                        session = requests.Session()
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
                        response_obj = session.get(summary_link, headers=headers)
                        soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

                        body = soup_obj.find('body')

                        table = body.find('div', id = 'quote-summary')
                        summary = table.find_all('tbody')

                        summary_left = summary[0].find_all('tr')
                        range_52 = summary_left[5].find_all('td')[1].text

                        summary_right = summary[1].find_all('tr')
                        market_cap = summary_right[0].find_all('td')[1].text

                        # parsing historical data
                        history_link = "https://finance.yahoo.com/quote/{ticker}/history?p={ticker}".format(ticker=ticker)
                        response_obj = session.get(history_link, headers=headers)
                        soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

                        body = soup_obj.find('body')
                        table = body.find('div', id = "Main")
                        table2 = table.find('tbody').find_all('tr', recursive=False)[0]
                        table_row = table2.find_all('td')
                        price = table_row[4].text
                        date = table_row[0].text

                        # parsing statistics data
                        statistics_link = "https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}".format(ticker=ticker)
                        response_obj = session.get(statistics_link, headers=headers)
                        soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

                        body = soup_obj.find('body')
                        table = body.find('div', id = "Main")
                        table2 = table.find('div', class_ = "Mstart(a) Mend(a)")
                        table3 = table2.find_all('div', recursive=False)[2]
                        net_income = table3.find_all('tr')[11].find_all('td')[1].text
                        current_ratio = table3.find_all('tr')[18].find_all('td')[1].text
                        total_equity = table3.find_all('tr')[17].find_all('td')[1].text

                        # append values to excel if found
                        df.iloc[index, 18] = price
                        df.iloc[index, 19] = range_52
                        df.iloc[index, 20] = market_cap
                        df.iloc[index, 21] = date
                        df.iloc[index, 22] = current_ratio
                        df.iloc[index, 23] = net_income
                        df.iloc[index, 24] = total_equity

                        print("Counter_yahoo: ", counter_yahoo)

                    except:
                        # append N/A value to excel, if ticker is not found
                        bag_of_empty.append(ticker)
                        nah = 'N/A'
                        df.iloc[index, 18] = nah
                        df.iloc[index, 19] = nah
                        df.iloc[index, 20] = nah
                        df.iloc[index, 21] = nah
                        df.iloc[index, 22] = nah
                        df.iloc[index, 23] = nah
                        df.iloc[index, 24] = nah
                else:
                    # append N/A value to excel, if ticker is wrong
                    nah = 'N/A'
                    df.iloc[index, 18] = nah
                    df.iloc[index, 19] = nah
                    df.iloc[index, 20] = nah
                    df.iloc[index, 21] = nah
                    df.iloc[index, 22] = nah
                    df.iloc[index, 23] = nah
                    df.iloc[index, 24] = nah        
            else:
                # append N/A value to excel, if ticker was already checked
                old_index = ticker_dict[ticker]  
                df.iloc[index, 18] = df.iloc[old_index, 18] 
                df.iloc[index, 19] = df.iloc[old_index, 19] 
                df.iloc[index, 20] = df.iloc[old_index, 20] 
                df.iloc[index, 21] = df.iloc[old_index, 21] 
                df.iloc[index, 22] = df.iloc[old_index, 22]
                df.iloc[index, 23] = df.iloc[old_index, 23]
                df.iloc[index, 24] = df.iloc[old_index, 24]
            
            if counter_yahoo == 10:       # to be deleted
                break

    yahoo_scraper_func()

    path = 'D:\\chromedriver'       # path to be changed
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
    driver = webdriver.Chrome(path, chrome_options=opts)

    # login credentials
    email = 'add_an_email'  # put your email
    password = 'manpower0'

    # opening browser
    url = 'https://www.moodys.com/'
    timeout = 20
    driver.maximize_window()
    driver.get(url)

    # opening dictionary with companies links
    my_dict_path = r'path\Companies_links.json' # add correct path
    with open(my_dict_path, 'r', encoding='utf8') as f:
            my_dict = json.load(f)

    # usefull variables
    links_dict = {}
    ticker_dict = {}
    maybe_bag = []
    fails_bag = []
    counter = 0
    new_counter = 0

    def class_parsing():
        class_url = new_url_base + "ratings/view-by-class"
        try:
            time.sleep(3)
            driver.get(class_url)
            time.sleep(3)
            sel_obj = driver.find_element_by_tag_name('body')
            time.sleep(1)
            action = webdriver.ActionChains(driver)
            driver.execute_script("window.scrollTo(0, window.scrollY + 480)")
            current = sel_obj.find_element_by_xpath('//tbody/tr[1]/td[2]/div[1]').text
        except:
            try:
                driver.navigate().refresh()
                time.sleep(10)                  
                wait = WebDriverWait(driver, timeout)
                childframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                sel_obj = driver.find_element_by_tag_name('body')
                time.sleep(1)
                action = webdriver.ActionChains(driver)
                driver.execute_script("window.scrollTo(0, window.scrollY + 480)")
                current = sel_obj.find_element_by_xpath('//tbody/tr[1]/td[2]/div[1]').text
            except:
                current = "NotFound"
                print('Current not found')
        df["Moody's Long Term Debt Rating"][index] = current
                
    def outlook_parsing():
        outlook_url = new_url_base + "ratings/issuer-outlook" 
        try:
            time.sleep(1)
            driver.get(outlook_url)
            time.sleep(1)
            sel_obj = driver.find_element_by_tag_name('body')
            outlook = sel_obj.find_element_by_xpath('//tbody/tr[1]/td[2]').text   
        except:
            try:
                driver.navigate().refresh()
                wait = WebDriverWait(driver, timeout)
                childframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
                time.sleep(10)
                sel_obj = driver.find_element_by_tag_name('body')
                outlook = sel_obj.find_element_by_xpath('//tbody/tr[1]/td[2]').text   
            except:
                outlook = "NotFound"
                print('Outlook not found')
        df["Moody's Outlook"][index] = outlook

    bag_of_useless = ['0', 'Rexnord Corporation', '\xa0', 'Private', ' ', '', 'nan', "Caliber Home Loans Inc."]

    # loging to my account
    time.sleep(1)
    sel_obj = driver.find_element_by_tag_name('body')
    login_button = sel_obj.find_element_by_xpath("//span[contains(text(),'LOG IN')]").click()

    time.sleep(1)
    register_box = driver.find_element_by_class_name("login-panel-container")
    username = register_box.find_elements_by_class_name("login-name")[0].find_element_by_tag_name('input').send_keys(email)
    password_field = register_box.find_elements_by_class_name("login-name")[1].find_element_by_tag_name('input').send_keys(password)

    cookies_accept = driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
    time.sleep(1)
    login_button2 = driver.find_element_by_xpath("//button[contains(text(),'LOG IN')]").click()

    # first iteration of every row in excel file
    for index, row in df.iterrows():
        ticker = str(row["Moody's Name"])
        class_value = str(row["Moody's Long Term Debt Rating"])
        outlook_value = str(row["Moody's Outlook"])

        if ticker not in ticker_dict:
            if ticker not in bag_of_useless:
                print(index, "\t", ticker)
                
                ticker_dict[ticker] = index
                counter += 1
                
                if ticker in my_dict:
                    new_url_base = my_dict[ticker]
                    pass
                else:
                    time.sleep(2)
                    sel_obj = driver.find_element_by_tag_name('body')
                    
                    # find search box and input company name
                    try:
                        search_field = sel_obj.find_element_by_class_name("search-box")
                        search_field2 = search_field.find_elements_by_tag_name('span')[0].click()
                        search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(ticker)
                    except:
                        time.sleep(3)
                        try:
                            sel_obj = driver.find_element_by_tag_name('body')
                            search_field = sel_obj.find_element_by_class_name("search-box")
                            search_field2 = search_field.find_elements_by_tag_name('span')[0].click()
                            search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(ticker)
                        except:
                            try:
                                driver.navigate().refresh()
                                time.sleep(5)
                                sel_obj = driver.find_element_by_tag_name('body')
                                search_field = sel_obj.find_element_by_class_name("search-box")
                                search_field2 = search_field.find_elements_by_tag_name('span')[0].click()
                                search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(ticker)
                            except:
                                try:
                                    driver.navigate().refresh()
                                    time.sleep(10)
                                    sel_obj = driver.find_element_by_tag_name('body')
                                    search_field = sel_obj.find_element_by_class_name("search-box")
                                    search_field2 = search_field.find_elements_by_tag_name('span')[0].click()
                                    search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(ticker)
                                except:
                                    fails_bag.append(ticker)
                                    pass
                    try:
                        time.sleep(3)
                        sel_obj = driver.find_element_by_tag_name('body')
                        company_link = sel_obj.find_element_by_class_name('search-widget').find_element_by_tag_name('a').click()
                    except:
                        time.sleep(3)
                        try:
                            search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(Keys.CONTROL,"a",Keys.DELETE).send_keys(ticker)
                            sel_obj = driver.find_element_by_tag_name('body')
                            company_link = sel_obj.find_element_by_class_name('search-widget').find_element_by_tag_name('a').click()
                        except:
                            try:
                                time.sleep(3)
                                search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(Keys.CONTROL,"a",Keys.DELETE).send_keys(ticker)
                                sel_obj = driver.find_element_by_tag_name('body')
                                company_link = sel_obj.find_element_by_class_name('search-widget').find_element_by_tag_name('a').click()
                            except:
                                try:
                                    driver.navigate().refresh()
                                    time.sleep(5)
                                    sel_obj = driver.find_element_by_tag_name('body')
                                    search_field = sel_obj.find_element_by_class_name("search-box")
                                    search_field2 = search_field.find_elements_by_tag_name('span')[0].click()
                                    search_field3 = search_field.find_element_by_class_name('search-box-inner').find_element_by_tag_name('input').send_keys(ticker)
                                    time.sleep(5)
                                    company_link = sel_obj.find_element_by_class_name('search-widget').find_element_by_tag_name('a').click()
                                except:
                                    maybe_bag.append(ticker)
                                    nah = 'NotFound'
                                    df.iloc[index, 26] = nah
                                    df.iloc[index, 28] = nah
                                    pass

                    # getting current url                
                    new_url = driver.current_url

                    first_element = new_url.find('reports?')
                    new_url_base = new_url.replace(new_url[first_element:], "")
                    
                    # excluding wrong url
                    bad_url = 'wwwmoodyscom'
                    if bad_url in new_url_base:
                        driver.get(url)
                        continue

                    # adding link to dictionary 
                    links_dict[ticker] = new_url_base

                # calling functions to find current and outlook values    
                class_parsing()
                outlook_parsing()

            else:
                nah = ''
                df.iloc[index, 26] = nah
                df.iloc[index, 28] = nah
                
        else:
            old_index = ticker_dict[ticker]  
            print("dict value: ", index)
            df.iloc[index, 26] = df.iloc[old_index, 26] 
            df.iloc[index, 28] = df.iloc[old_index, 28]

        if counter == 20:         # to be deleted
            break

        if index % 50 == 0:
            time.sleep(5)
    
    # collecting info about NotFound values in first iteration
    current_first_nf = df.loc[df["Moody's Long Term Debt Rating"] == 'NotFound'].count()["Moody's Long Term Debt Rating"]
    outlook_first_nf = df.loc[df["Moody's Outlook"] == 'NotFound'].count()["Moody's Outlook"]
    
    # second iteration to collect more current and outlook values
    for index, row in df.iterrows():
        ticker = str(row["Moody's Name"])
        class_value = str(row["Moody's Long Term Debt Rating"])
        outlook_value = str(row["Moody's Outlook"])

        if ticker not in bag_of_useless:
            new_url_base = my_dict[ticker]

            # class parsing
            if class_value == "NotFound":
                new_counter += 1        # to be deleted
                class_parsing()
            
            # outlook parsing
            if outlook_value == "NotFound":
                new_counter += 1        # to be deleted  
                outlook_parsing()

        if new_counter == 20:          # to be deleted
            break

    # creating dictionary with new links    
    with open('Companies_links_new.json', 'w') as f:
        json.dump(links_dict, f)

    # info purposes 
    current_second_nf = df.loc[df["Moody's Long Term Debt Rating"] == 'NotFound'].count()["Moody's Long Term Debt Rating"]
    outlook_second_nf = df.loc[df["Moody's Outlook"] == 'NotFound'].count()["Moody's Outlook"]
    print("\nMaybe bag: ", maybe_bag)
    print('Number of elements: ', len(maybe_bag))
    print("Fails bag: ", fails_bag)
    print('Number of elements: ', len(fails_bag))
    print("Current first nf: ", current_first_nf)
    print("Current second nf: ", current_second_nf)
    print("Difference: ", current_first_nf - current_second_nf)
    print("Outlook first nf: ", outlook_first_nf)
    print("Outlook second nf: ", outlook_second_nf)
    print("Difference: ", outlook_first_nf - outlook_second_nf)
    print('Total rows: ', index)
    print('Processed values: ', counter, '\n')

    driver.close()
    new_file_path = ('path\file_name {}.xlsx'.format(datetime.datetime.now().strftime("%d_%m_%y %H_%M_%S")))     # this path should be changed
    df.to_excel(new_file_path, index = False)
    
    return new_file_path

file_name = r'path\master_file_name.xlsx'      # this path should be changed
moodys_scraper_func(file_name)    
