import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import functools
import datetime

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        end_hour = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs at {end_hour}. It took {time.strftime('%H:%M:%S', time.gmtime(run_time))}.")
        return value
    return wrapper_timer

class yahoo_scraper_class:
    def __init__(self, file_name):
        self.file_name = file_name

    @timer
    def yahoo_scraper_func(self):
        df = pd.read_excel(file_name)
        ticker_dict = {}
        counter = 0
        new_counter = 0

        bag_of_useless = ['Private', 'Foreign Owned', '-', 'n/a', 'Government', 'HSE.TO','GTES', ' ARD', 'Privately held by MMJ Group Holdings Limited (MMJJF), an Austrailian-listed company.', "Gov't", 'None', 'Non-Profit', '', 'Foreign Parent-9375.T ticker?', "State Gov't",  'GPS (The GAP)', 'Tribal Government', 'Bankruptcy', 'Private Equity', 'Private?', 'Non-profit organization', 'N/a', 'Sumitomo Mitsui Trust Holdings Inc.', '532540 (India: Bombay)', 'VLVLY (TICKER)  / VOLVY (MOODYS)', '2162 (JASDAQ)', 'RCRUY (parent)', 0, 'Province of Quebec', 'UTX', 'VLVY', 'Foreign Parent', 'Goverment', 'MIK', 'private', 'Foreign', 'RTIX/SRGA', 'SAMSNG', 'SEB SA', 'HSE', 'SIE', ' ', 'VSVS', 'VOLVY', 'BRK', '\xa0', 'HINDALCO', 'Fed Owned', 'AEXAY (parent)', 'C ', 'NEMTF', 'CSGN', 'SDF', ' LH', 'NEOS', 'GAS', 'CVIA', 'FCAU', 'ETH', 'JASN', 'IEP (Parent)', 'PRSC', 'CLGX']
        maybe_bag = ['2162 (JASDAQ)', 'RCRUY (parent)']
        bag_of_empty = []

        for index, row in df.iterrows():
            ticker = row['Ticker'] 
            print('Row: ', index)
            
            if ticker not in ticker_dict:
                if ticker not in bag_of_useless:
                    try:
                        ticker_dict[ticker] = index
                        counter += 1

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

                        df.iloc[index, 18] = price
                        df.iloc[index, 19] = range_52
                        df.iloc[index, 20] = market_cap
                        df.iloc[index, 21] = date
                        df.iloc[index, 22] = current_ratio
                        df.iloc[index, 23] = net_income
                        df.iloc[index, 24] = total_equity

                        print("Counter: ", counter)

                    except:
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
                    nah = 'N/A'
                    df.iloc[index, 18] = nah
                    df.iloc[index, 19] = nah
                    df.iloc[index, 20] = nah
                    df.iloc[index, 21] = nah
                    df.iloc[index, 22] = nah
                    df.iloc[index, 23] = nah
                    df.iloc[index, 24] = nah        
            else:
                old_index = ticker_dict[ticker]  
                print("dict value: ", index)
                df.iloc[index, 18] = df.iloc[old_index, 18] 
                df.iloc[index, 19] = df.iloc[old_index, 19] 
                df.iloc[index, 20] = df.iloc[old_index, 20] 
                df.iloc[index, 21] = df.iloc[old_index, 21] 
                df.iloc[index, 22] = df.iloc[old_index, 22]
                df.iloc[index, 23] = df.iloc[old_index, 23]
                df.iloc[index, 24] = df.iloc[old_index, 24]
                        
            # if counter == 2:
            #     break
        df.to_excel('Master Template Credit {}.xlsx'.format(datetime.datetime.now().strftime("%d_%m_%y %H_%M_%S"), index = False))
        print("Bag of empty includes: ", bag_of_empty)
        print('Number of unique values: ', counter)



file_name = 'Master Template Credit Flash_0716.xlsx'

yahoo = yahoo_scraper_class(file_name)
yahoo.yahoo_scraper_func()