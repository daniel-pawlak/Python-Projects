# from os import link
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import requests
# import regex as re
import pandas as pd
import time
import functools
import datetime
import json
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 

path = 'D:\\chromedriver'
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
driver = webdriver.Chrome(path, chrome_options=opts)
# driver = webdriver.Chrome(path)

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
            print(f"\n\nATTENTZIONE\n\n{func.__name__} failed after {run_time:.4f} secs at {end_hour}. It took {time.strftime('%H:%M:%S', time.gmtime(run_time))}.\n\nUnexpected {err=}, {type(err)=}\n\n")
            
    return wrapper_timer

@timer
def moodys_scraper_func(file_name):
    email = 'daniel.pawlak@manpowergroup.com'
    password = 'manpower0'
    url = 'https://www.moodys.com/'
    timeout = 20
    driver.maximize_window()
    driver.get(url)

    df = pd.read_excel(file_name)
    
    links_dict = {}
    ticker_dict = {}
    maybe_bag = []
    fails_bag = []
    counter = 0

    bag_of_useless = ['0', 'Rexnord Corporation', '\xa0', 'Private', ' ', '', 'nan']

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

    for index, row in df.iterrows():
        ticker = str(row["Moody's Name"])

        if ticker not in ticker_dict:
            if ticker not in bag_of_useless:
                print(index, "\t", ticker)
                
                ticker_dict[ticker] = index
                counter += 1
                time.sleep(2)
                sel_obj = driver.find_element_by_tag_name('body')
                
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
            
                new_url = driver.current_url

                first_element = new_url.find('reports?')
                new_url_base = new_url.replace(new_url[first_element:], "")
                
                # testing new solution
                links_dict[ticker] = new_url_base

                class_url = new_url_base + "ratings/view-by-class"
                outlook_url = new_url_base + "ratings/issuer-outlook"

                # class parsing
                try:
                    time.sleep(3)
                    driver.get(class_url)
                    time.sleep(3)
                    sel_obj = driver.find_element_by_tag_name('body')
                    time.sleep(1)
                    # sel_obj.send_keys(Keys.PAGE_DOWN)
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
                        # sel_obj.send_keys(Keys.PAGE_DOWN)
                        action = webdriver.ActionChains(driver)
                        driver.execute_script("window.scrollTo(0, window.scrollY + 480)")
                        current = sel_obj.find_element_by_xpath('//tbody/tr[1]/td[2]/div[1]').text
                    except:
                        current = "NotFound"
                        print('Current not found')

                # outlook parsing
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

                df.iloc[index, 26] = current
                df.iloc[index, 28] = outlook

            else:
                nah = 'N/A useless'
                df.iloc[index, 26] = nah
                df.iloc[index, 28] = nah
                
        else:
            old_index = ticker_dict[ticker]  
            print("dict value: ", index)
            df.iloc[index, 26] = df.iloc[old_index, 26] 
            df.iloc[index, 28] = df.iloc[old_index, 28]

        # info only
        if counter % 50 == 0 and counter != 0:
            print("Counter is: \n\n", counter, "\n\n")
        # if counter == 3:
        #     break

    df.to_excel('Master Template Credit Moodys {}.xlsx'.format(datetime.datetime.now().strftime("%d_%m_%y %H_%M_%S")), index = False)
    driver.close()

    with open('Companies_links.json', 'w') as f:
        json.dump(links_dict, f)

    # info purposes 
    print("\nMaybe bag: ", maybe_bag)
    print('Number of elements: ', len(maybe_bag))
    print("Fails bag: ", fails_bag)
    print('Number of elements: ', len(fails_bag))
    print("Not found Current: ", df.loc[df["Moody's Long Term Debt Rating"] == 'NotFound'].count()["Moody's Long Term Debt Rating"])
    print("Not found Outlook: ", df.loc[df["Moody's Outlook"] == 'NotFound'].count()["Moody's Outlook"], '\n')
    print('Total rows: ', index)
    print('Processed values: ', counter, '\n')

file_name = r'C:\Users\danie\Dropbox\Python\Scrapers\Yahoo\Master Template Credit Flash_0716_new.xlsx'

moodys_scraper_func(file_name)    