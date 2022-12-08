from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import functools
import datetime
import json
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
# warnings.filterwarnings("ignore", category=UserWarning)

path = 'D:\\chromedriver'
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
driver = webdriver.Chrome(path, chrome_options=opts)

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
    email = 'add_email
    password = 'add_pwd'
    url = 'https://www.moodys.com/'
    timeout = 20
    driver.maximize_window()
    driver.get(url)

    my_dict_path = r'path\Companies_links.json'
    with open(my_dict_path, 'r', encoding='utf8') as f:
            my_dict = json.load(f)

    df = pd.read_excel(file_name)

    links_dict = {}
    ticker_dict = {}
    maybe_bag = []
    fails_bag = []
    counter = 0
    new_counter = 0

    def class_parsing():
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
                
                if ticker in my_dict:
                    new_url_base = my_dict[ticker]
                    pass
                else:
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
                    
                    #excluding wrong url
                    bad_url = 'wwwmoodyscom'
                    if bad_url in new_url_base:
                        driver.get(url)
                        continue

                    # testing dictionaries
                    links_dict[ticker] = new_url_base
                class_parsing()
                outlook_parsing()

            else:
                nah = 'N/A'
                df.iloc[index, 26] = nah
                df.iloc[index, 28] = nah
                
        else:
            old_index = ticker_dict[ticker]  
            print("dict value: ", index)
            df.iloc[index, 26] = df.iloc[old_index, 26] 
            df.iloc[index, 28] = df.iloc[old_index, 28]

        if counter == 20:
            break
        if index % 50 == 0:
            time.sleep(5)
    
    current_first_nf = df.loc[df["Moody's Long Term Debt Rating"] == 'NotFound'].count()["Moody's Long Term Debt Rating"]
    outlook_first_nf = df.loc[df["Moody's Outlook"] == 'NotFound'].count()["Moody's Outlook"]
    
    for index, row in df.iterrows():
        ticker = str(row["Moody's Name"])
        class_value = str(row["Moody's Long Term Debt Rating"])
        outlook_value = str(row["Moody's Outlook"])

        if ticker not in bag_of_useless:
            new_url_base = my_dict[ticker]

            # class parsing
            if class_value == "NotFound":
                new_counter += 1
                class_url = new_url_base + "ratings/view-by-class"
                class_parsing()
            
            # outlook parsing
            if outlook_value == "NotFound":
                counter += 1
                outlook_url = new_url_base + "ratings/issuer-outlook"    
                outlook_parsing()
        if new_counter == 20:
            break
        
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
    new_file_path = ('path\final_file_name {}.xlsx'.format(datetime.datetime.now().strftime("%d_%m_%y %H_%M_%S")))  
    df.to_excel(new_file_path, index = False)
    
    return new_file_path

file_name = r'path\master_file_name.xlsx'
moodys_scraper_func(file_name)    
