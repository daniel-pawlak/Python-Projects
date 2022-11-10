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

@timer
def yahoo_scraper_func():
    ticker = 'UPS'

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

    price1 = body.find('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    print(price1)
    print(price)
    print(range_52)
    print(market_cap)
    print(date)
    print(current_ratio)
    print(net_income)
    print(total_equity)

yahoo_scraper_func()