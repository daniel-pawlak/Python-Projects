"""Manipulation of excel file downloaded from ______ based on RM Data Formatting file"""
import pandas as pd
import numpy as np
import datetime
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

def open_file(file_name, header=0, format='excel', final=False):
    if format == 'excel':
        if header == 0:
            if final == False:
                df = pd.read_excel(file_name)
            else:
                # df = pd.read_excel(file_name, sheet_name='Weekly File (2)')
                df = pd.read_excel(file_name, sheet_name='Weekly')

        else:
            df = pd.read_excel(file_name, sheet_name='Summary', header=header)
    else:  
        df = pd.read_csv(file_name, header=header,encoding='unicode_escape') 
   
    return df

def delete_columns(df, columns_list):
    df = df.drop(columns=columns_list)
    return df

def add_columns_values(df, column_name, columns):
    if not df[columns[0]].empty and not df[columns[1]].empty:
        df[column_name] = df[columns[0]] + df[columns[1]]
    elif not df[columns[0]].empty and df[columns[1]].empty:
        df[column_name] = df[columns[0]]
    elif df[columns[0]].empty and not df[columns[1]].empty:
        df[column_name] = df[columns[1]]

    return df

def add_column(df, column, value, position):
    # df, column name, column value, column position
    df[column] = value
    df = move_column(df, column, position)
    return df

def move_column(df, column, position):
    column_to_move = df.pop(column)
    # insert column with insert(location, column_name, column_value)
    df.insert(position, column, column_to_move)
    return df

def renaming_values(df, column, value1, value2):
    # df, column to change, value1 to be changed, value2 as a new one
    df[column] = df[column].str.replace(value1, value2)
    return df

def filtering_values(df, column1, column2, column3, value1, value2, type):
    #df, column1 to be filtered, column2 to be filled, column3 for subtraction, value1 to be checked, value2 to be added, type of comparision
    if type == "=":
        df.loc[df[column1] == value1, column1] = value2
    elif type == ">":
        df.loc[df[column1] >= value1, column2] = value2
    elif type == "-":
        df.loc[(df[column1] - df[column3]) >= value1, column2] = value2

    return df

def concat_columns(df):
    # concatenate values from few columns
    # UGLY
    df['CONCAT'] = df['System'] + df['US - CAN'] + df['LOB'] + df['Roll-up Client Name'] + df['Client Name']
    return df

def delete_20k(df):
    # delete rows without >$20k value
    df['Reason for Review'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Reason for Review'], inplace=True)
    return df

def delete_empty_customer(df):
    # delete rows without any value in Customer Number
    df['Customer Number'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Customer Number'], inplace=True)
    return df

def merge_dataframes(df1, df2, df3=0, df=True):
    if df != True:
        # merge two dfs into one
        df = df1.append(df2, ignore_index=True)
    else:
        # merge three dfs into one
        df4 = df1.append(df2, ignore_index=True)
        df = df4.append(df3, ignore_index=True)
    return df

def compare_two_df(df1, df2, column1, column2, column3, column4, column5='', column6='', two_cols=1):
    # at this point we have two dataframes with the same number of rows, and maybe different indexes
    # drop the indexes of both, so we can compare the dataframes and other operations like update etc.
    df1.reset_index(drop=True, inplace=True)

    df2.drop_duplicates(subset=column2, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    
    # compare the column1 of df1 and column2 of df2, and update the column3 of df1 with column4 of df2 if they match, else None
    df  = pd.merge(left=df1, right=df2, how='left', left_on=column1, right_on=column2)

    for row in df1.index:
        if df1.iloc[row][column3] == '' or df1.iloc[row][column3] == '-' or pd.isnull(df1.loc[row][column3]):
                df1.at[row, column3] = df.iloc[row][column4]

        if two_cols==2:
            if df1.iloc[row][column5] == '' or df1.iloc[row][column5] == '-' or pd.isnull(df1.loc[row][column5]):
                df1.at[row, column5] = df.iloc[row][column6] 

    return df1

def export_file(df, name, path):
    end_hour = datetime.datetime.now().strftime('%H_%M_%S')
    new_file_path = ('{}{}_{}.xlsx'.format(path, name, end_hour))
    df.to_excel(new_file_path, index = False)

def open_ps(path, name):
    file_name = path + name
    df = open_file(file_name)

    df = add_column(df, 'Reason for Review', '', 0)
    df = add_column(df, 'CONCAT', '', 1)
    df = add_column(df, 'System', 'PS', 2)
    df = add_column(df, 'Last Pymt Date', '', len(df.columns))
    df = add_column(df, 'Last Inv Date', '', len(df.columns))
    df = add_column(df, 'Credit Limit', '', len(df.columns))
    
    # rename columns 
    df = df.rename(columns={"US/CAN": "US - CAN", 'ROLL-UP LOB':'LOB','ROLL-UP CLIENT':'Roll-up Client Name', 'Bill To Customer Name':'Client Name','Bill To Customer Number':'Customer Number',
                            ' Total AR':'Total AR',' 1-10': '1-10 Days PD', ' 11-30':'11-30 Days PD', ' 31-60':'31-60 Days PD',
                            ' 61-90':'61-90 Days PD', ' 91-180':'91-180 Days PD', ' 180+':'180+ Days PD', 
                            ' 30+':'30+ Past Due', ' Current':'Current'})

    # filter data in Total AR, if >50 k then add info to Reason for review, (df, column1 to be filtered, column2 to be filled, value1 to be checked, value2 to be added, type of comparision)   
    df = filtering_values(df, 'Total AR', 'Reason for Review', '', 50000, ">$50K AR", ">")

    df = delete_20k(df)               

    return df

def open_rmps(path, name):
    file_name = path + name
    df = open_file(file_name, header=1)

    # strip column names
    df = df.rename(columns=lambda x: x.strip())

    # columns to be deleted
    columns_list = ['11+ Past Due', '90+ Past Due', 'Collector', 'Bill Type']
    df = df.drop(df.columns[[5, 6]],axis = 1)
    df = delete_columns(df, columns_list)
    column_name = '180+ Days PD'
    columns = ['181-365 Days PD', '365+ Days PD']
    df.fillna(0)
    df = add_columns_values(df, column_name, columns)
    df = delete_columns(df, columns)

    column = '30+ Past Due'
    position = len(df.columns)-1
    df  = move_column(df, column, position)

    df = renaming_values(df, 'Unit', '063|030', '')
   
    column = "Customer #"
    position = df.columns.get_loc('Name')
    df  = move_column(df, column, position)

    df = add_column(df, 'Reason for Review', '', 0)
    df = add_column(df, 'CONCAT', '', 1)
    df = add_column(df, 'System', 'RM PS', 2)
    df = add_column(df, 'LOB', 'RIGHT MGMT', 4)
    df = add_column(df, 'Roll-up Client Name', '', 5)
    df = move_column(df, 'Name', 6)
    df = move_column(df, 'Grand Total', 8)
    df = add_column(df, 'Last Pymt Date', '', len(df.columns))
    df = add_column(df, 'Last Inv Date', '', len(df.columns))
    df = add_column(df, 'Credit Limit', '', len(df.columns))
    
    # rename columns 
    df = df.rename(columns={"Unit": "US - CAN", 'Name': 'Client Name', 'Grand Total':"Total AR", "Customer #":'Customer Number'})

    # filter data in Total AR, if >50 k then add info to Reason for review, (df, column1 to be filtered, column2 to be filled, value1 to be checked, value2 to be added, type of comparision)   
    df = filtering_values(df, 'Total AR', 'Reason for Review', '', 50000, ">$50K AR", ">")

    # delete rows without >$50k value
    df = delete_20k(df)

    return df

def open_canada(path, name):
    file_name = path + name
    df = open_file(file_name, header = 6, format='csv')

    # add Entity column
    column = "US - CAN"
    value = 'CAN'
    position = 0
    df = add_column(df, column, value, position)
    return df

def open_us(path, name):
    file_name = path + name
    df = open_file(file_name, header = 5, format='csv')
    
    # add "US - CAN" column
    column = "US - CAN"
    value = 'US'
    position = 0
    df = add_column(df, column, value, position)
    return df
    
def jde_processing(path, name_can, name_us):
    df = merge_dataframes(open_canada(path, name_can), open_us(path, name_us), df=False)
    
    # delete columns
    columns_list = ["Manager", "Collector", "Cust. Own B.U.", 'Long Address', 'Over 11 Days', 'Total Past Due Amount', \
                    'Last Note Date', 'Cst Grp', 'Mgr Code', 'Coll Mgr Code', 'Invoice Output Type', 'E-Mail Address']   
    df = delete_columns(df, columns_list)

    # add columns 'Reason for review', 'Concat', 'System' and 'LOB' with value MANPOWER in the 2nd column
    df = add_column(df, 'LOB', 'MANPOWER', 1)
    df = add_column(df, 'Reason for Review', '', 0)
    df = add_column(df, 'CONCAT', '', 1)
    df = add_column(df, 'System', 'JDE', 2)

    # move Group Code to column 6
    df = move_column(df, 'Group Code Name', 5)
    # move Customer Name to column 7
    df = move_column(df, 'Customer Name', 6)

    # move Total AR to column 9
    df = move_column(df, 'Total AR', 8)
    df = add_column(df, 'Current', '', 9)

    # filter data in Group Code Name, change Not Applicable to Customer Name if Group Code Name == Not Applicable
    # df =  filtering_values(df, 'Group Code Name', 'Customer Name', '', 'Not Applicable', df['Customer Name'], "=")
    
    df =  filtering_values(df, 'Group Code Name', '', '', 'Not Applicable', df['Customer Name'], "=")

    # delete any character that is not a number or letter from Total AR
    df = renaming_values(df, 'Total AR', '[^A-Za-z0-9]+', '')

    # replace empty cells with 0
    df.loc[df['Total AR'].isnull(),'Total AR'] = 0

    # change cells type to int
    df['Total AR'] = df['Total AR'].astype('int')

    # filter data in Total AR, if >50 k then add info to Reason for review, (df, column1 to be filtered, column2 to be filled, value1 to be checked, value2 to be added, type of comparision)   
    df =  filtering_values(df, 'Total AR', 'Reason for Review', '', 50000, ">$50K AR", ">")

    # filter data, if Total AR - Credit Limit >20 k then add info to Reason for review, (df, column1 to be filtered, column2 to be filled, value1 to be checked, value2 to be added, type of comparision)   
    # df =  filtering_values(df, 'Total AR', 'Reason for Review', 'Credit Limit', df['Credit Limit'], ">$20K OVER CL", "-")
    df =  filtering_values(df, 'Total AR', 'Reason for Review', 'Credit Limit', 20000, ">$20K OVER CL", "-")

    # rename columns
    df = df.rename(columns={'1 to 10 Days': '1-10 Days PD', '11 to 30 Days':'11-30 Days PD', '31 to 60 Days':'31-60 Days PD',
                            '61 to 90 Days':'61-90 Days PD', '91 to 180 Days':'91-180 Days PD', 'Over 180 Days':'180+ Days PD', 
                            'Total Over 30 Days':'30+ Past Due', 'Last Pmt Date':'Last Pymt Date', 'Last Invoice Date':'Last Inv Date', 
                            'Customer Name':'Client Name', 'Group Code Name':'Roll-up Client Name', 'JDE Customer Number':'Customer Number'})
    
    # delete 'Within Terms' column, as it is not in Master template
    df = delete_columns(df, ['Within Terms'])
    # delete rows where value is less than $20k
    df = delete_20k(df)
    df = df.fillna('-')

    return df

def open_master(path, name):
    file_name = path + name
    df = open_file(file_name, header = 0, format='excel', final=True)

    df = df.rename(columns={'datetime.datetime(2021, 1, 10, 0, 0)': '1-10 Days PD', 'datetime.datetime(2021, 11, 30, 0, 0)':'11-30 Days PD', '31-60':'31-60 Days PD',
                        '61-90':'61-90 Days PD', '91-180':'91-180 Days PD', '181+':'180+ Days PD', 
                        '30+':'30+ Past Due', ' Current':'Current'})
  
    # Changing columns name with index number
    df.columns.values[10] = '1-10 Days PD'
    df.columns.values[11] = '11-30 Days PD'

    return df

def open_ps_date(path, name):
    # open file with dates of invoices
    file_name = path + name
    df = pd.read_excel(file_name, sheet_name='BASE FILE', header=1)  
           
    # columns to be deleted
    columns_list = ['Customer Name', 'Item ID', 'Item Amount', 'Payment Amount']
    
    df = delete_columns(df, columns_list)

    return df

def yahoo_scraper_func(df):
    """BeautifulSoup scraper which goes to yahoo finance site and grabs needed data, then inserts to given dataframe"""
    # add few columns
    df = add_column(df, 'Stock Price', '', 30)
    df = add_column(df, '52 Week Range', '', 31)
    df = add_column(df, 'Market Cap', '', 32)
    df = add_column(df, 'Date of Data (Quarterly financial data)', '', 33)
    df = add_column(df, 'Current Ratio', '', 34)
    df = add_column(df, 'Net Income', '', 35)
    df = add_column(df, 'Shareholder Equity', '', 36)

    ticker_dict = {}

    bag_of_useless = ['','Private', 'Foreign Owned', 'HSE.TO', ' ARD', '-', 0, 'Privately held by MMJ Group Holdings Limited (MMJJF), an Austrailian-listed company.',\
         'Government', "Gov't", 'None', 'Province of Quebec', 'UTX', 'VLVY', 'Foreign Parent', 'FLOW', 'HOME', 'BLL', 'Non-Profit', 'Goverment',\
             'MIK', 'RCRUY (parent)', 'FBHS', 'Foreign Parent-9375.T ticker?', "State Gov't", 'INOV', 'DAI.DE', 'NELES.HE', 'GPS (The GAP)',\
                 'Tribal Government', 'Bankruptcy', 'Foreign', 'RXN', 'RRD', 'RTIX/SRGA', 'SAMSNG', 'SEB SA', 'HSE', 'SIE', ' ', '2162 (JASDAQ)',\
                     'Private Equity', 'VSVS', 'VOLVY', 'BRK', '\xa0', 'HINDALCO', 'Fed Owned', 'ATRS', 'AEXAY (parent)', 'C ', 'Private?', 'CSGN',\
                         'UFS', 'Non-profit organization', 'SDF', ' LH', 'MDLA', 'NEOS', 'GAS', 'PBCT', 'PPD', 'CVIA',\
                             'Sumitomo Mitsui Trust Holdings Inc.', 'PDRDY', '532540 (India: Bombay)', 'TVTY', 'JW-A', 'FCAU', 'ETH', 'JASN',\
                                 'IEP (Parent)', 'PRSC', 'HRC', 'HFC', 'QCOM', 'SNAP', 'SPWR', 'ZION', 'BCKIF', 'CLGX', 'HAS', 'MRVL', 'QBIEY',\
                                     'RCL', 'CVX', 'EQNR', 'IMO', 'AMT', 'ANTM', 'AVNS', 'AVNT', 'BBBY', 'BDC', 'BK', 'CPRI', 'CLVT', 'CCI', 'DAL',\
                                         'XRAY', 'DFS', 'DLB', 'EFX', 'EXC', 'HUM', 'MSI', 'NOK', 'NOC', 'PZZA', 'PYPL', 'PSO', 'RSG', 'RYDAF',\
                                             'SPLK', 'SYF', 'HO.PA', 'TKR', 'TSCO', 'UIS', 'VLVLY (TICKER)  / VOLVY (MOODYS)', 'WBS']
    bag_of_empty = []

    for index, row in df.iterrows():
        ticker = row['Ticker'] 
        
        if ticker not in ticker_dict:
            if ticker not in bag_of_useless:
                try:
                    ticker_dict[ticker] = index

                    # parsing summary data
                    summary_link = "https://finance.yahoo.com/quote/{ticker}?p={ticker}".format(ticker=ticker)
                    
                    # BS4 on a ticker page
                    session = requests.Session()
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
                    response_obj = session.get(summary_link, headers=headers)
                    soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

                    body = soup_obj.find('body')

                    table = body.find('div', id = 'quote-summary')
                    summary = table.find_all('tbody')

                    summary_left = summary[0].find_all('tr')

                    # range 52
                    range_52 = summary_left[5].find_all('td')[1].text

                    summary_right = summary[1].find_all('tr')

                    # market cap
                    market_cap = summary_right[0].find_all('td')[1].text

                    # parsing historical data
                    history_link = "https://finance.yahoo.com/quote/{ticker}/history?p={ticker}".format(ticker=ticker)
                    response_obj = session.get(history_link, headers=headers)
                    soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

                    body = soup_obj.find('body')
                    table = body.find('div', id = "Main")
                    table2 = table.find('tbody').find_all('tr', recursive=False)[0]
                    table_row = table2.find_all('td')

                    # closing price
                    price = table_row[4].text
                    # if no closing price, add current price
                    if price == '-':
                        price = body.find('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text

                    # date
                    date = table_row[0].text

                    # parsing statistics data
                    statistics_link = "https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}".format(ticker=ticker)
                    response_obj = session.get(statistics_link, headers=headers)
                    soup_obj = BeautifulSoup(response_obj.content, 'html.parser')

                    # accessing data
                    body = soup_obj.find('body')
                    table = body.find('div', id = "Main")
                    table2 = table.find('div', class_ = "Mstart(a) Mend(a)")
                    table3 = table2.find_all('div', recursive=False)[2]

                    # net income
                    net_income = table3.find_all('tr')[11].find_all('td')[1].text

                    # current ratio
                    current_ratio = table3.find_all('tr')[18].find_all('td')[1].text

                    # total equity
                    total_equity = table3.find_all('tr')[17].find_all('td')[1].text

                    df.loc[index, 'Stock Price'] = price
                    df.loc[index, '52 Week Range'] = range_52
                    df.loc[index, 'Market Cap'] = market_cap
                    df.loc[index, 'Date of Data (Quarterly financial data)'] = date
                    df.loc[index, 'Current Ratio'] = current_ratio
                    df.loc[index, 'Net Income'] = net_income
                    df.loc[index, 'Shareholder Equity'] = total_equity

                except:
                    bag_of_empty.append(ticker)
                    nah = 'N/A'
                    df.loc[index, 'Stock Price'] = nah
                    df.loc[index, '52 Week Range'] = nah
                    df.loc[index, 'Market Cap'] = nah
                    df.loc[index, 'Date of Data (Quarterly financial data)'] = nah
                    df.loc[index, 'Current Ratio'] = nah
                    df.loc[index, 'Net Income'] = nah
                    df.loc[index, 'Shareholder Equity'] = nah
            else:
                nah = 'N/A'
                df.loc[index, 'Stock Price'] = nah
                df.loc[index, '52 Week Range'] = nah
                df.loc[index, 'Market Cap'] = nah
                df.loc[index, 'Date of Data (Quarterly financial data)'] = nah
                df.loc[index, 'Current Ratio'] = nah
                df.loc[index, 'Net Income'] = nah
                df.loc[index, 'Shareholder Equity'] = nah        
        else:
            old_index = ticker_dict[ticker]  

            df.loc[index, 'Stock Price'] = df.loc[old_index, 'Stock Price'] 
            df.loc[index, '52 Week Range'] = df.loc[old_index, '52 Week Range'] 
            df.loc[index, 'Market Cap'] = df.loc[old_index, 'Market Cap'] 
            df.loc[index, 'Date of Data (Quarterly financial data)'] = df.loc[old_index, 'Date of Data (Quarterly financial data)'] 
            df.loc[index, 'Current Ratio'] = df.loc[old_index, 'Current Ratio']
            df.loc[index, 'Net Income'] = df.loc[old_index, 'Net Income']
            df.loc[index, 'Shareholder Equity'] = df.loc[old_index, 'Shareholder Equity']

    return df

@timer
def make_final_file(path, ps_name, rmps_name, can_name, us_name, master_name, ps_date_name, final_name):
    # merge 3 files into one and export it
    df1 = open_ps(path, ps_name)
    df2 = open_rmps(path, rmps_name)
    df3 = jde_processing(path, can_name, us_name)
    df = merge_dataframes(df1, df2, df3)

    # concatenate values from few columns
    df = concat_columns(df)

    # sort values in Total AR in ascending (A-Z) order
    df = df.sort_values(by=['Total AR'])

    df_master = open_master(path, master_name)

    df_merged = merge_dataframes(df_master, df, df=False)
    df_ps_date = open_ps_date(path, ps_date_name)

    df_merged['Customer Number'] = df_merged['Customer Number'].astype('str')
    df_ps_date['Customer ID'] = df_ps_date['Customer ID'].astype('str')

    df_merged = renaming_values(df_merged, 'Customer Number', '^000', '')
    df_ps_date = renaming_values(df_ps_date, 'Customer ID', '^000', '')

    df_final = compare_two_df(df_merged, df_ps_date, 'Customer Number', 'Customer ID', 'Last Inv Date', 'Item Date', 'Last Pymt Date', 'Payment Date', two_cols=2)

    df_final = renaming_values(df_final, 'Customer Number', '^000', '')
    df_final = renaming_values(df_final, 'Customer Number', '.0$', '')

    # update Ticker from Master file to Final file
    df_nums = df_master[['Customer Number', 'Ticker',"Moody's Name", "Moody's Long Term Debt Rating","Moody's Outlook","Internal Notes"]]
    df_nums = renaming_values(df_nums, 'Customer Number', '^000', '')
    df_nums = df_nums.drop_duplicates(subset=['Customer Number'])
    df_nums['Customer Number'].dropna(inplace=True)
    
    df_final = compare_two_df(df_final, df_nums, 'Customer Number', 'Customer Number', 'Ticker', 'Ticker_y')

    df_final = pd.merge(df_final, df_nums, on ='Customer Number', how ='left')

    df_final.loc[df_final['Ticker_x'].isnull(),'Ticker_x'] = df_final['Ticker_y']
    df_final.loc[df_final["Moody's Name_x"].isnull(),"Moody's Name_x"] = df_final["Moody's Name_y"]
    df_final.loc[df_final["Moody's Long Term Debt Rating_x"].isnull(),"Moody's Long Term Debt Rating_x"] = df_final["Moody's Long Term Debt Rating_y"]
    df_final.loc[df_final["Moody's Outlook_x"].isnull(),"Moody's Outlook_x"] = df_final["Moody's Outlook_y"]
    df_final.loc[df_final['Internal Notes_x'].isnull(),'Internal Notes_x'] = df_final['Internal Notes_y']

    df_final = delete_columns(df_final, ['Ticker_y', "Moody's Name_y", "Moody's Long Term Debt Rating_y", "Moody's Outlook_y", 'Internal Notes_y'])
    
    # rename columns
    df_final = df_final.rename(columns={'Ticker_x': 'Ticker', "Moody's Name_x": "Moody's Name", 
                                        "Moody's Long Term Debt Rating_x": "Moody's Long Term Debt Rating",
                                        "Moody's Outlook_x": "Moody's Outlook",
                                        'Internal Notes_x': 'Internal Notes'})

    # change datetime to american format
    try:
        df_final['Last Inv Date'] = pd.to_datetime(df_final['Last Inv Date'].astype('str'), errors ='coerce')
        df_final['Last Inv Date'] = df_final['Last Inv Date'].dt.strftime('%m/%d/%Y')

        df_final['Last Pymt Date'] = pd.to_datetime(df_final['Last Pymt Date'].astype('str'), errors ='coerce')
        df_final['Last Pymt Date'] = df_final['Last Pymt Date'].dt.strftime('%m/%d/%Y')
    except:
        pass

    # change Reason for Review for TAPFIN EXT
    df_final.loc[(df_final['Total AR'] >= 2000000) & (df_final['LOB'] == 'TAPFIN EXT'), 'Reason for Review'] = '>$2M'
    df_final.loc[(df_final['Total AR'] < 2000000) & (df_final['LOB'] == 'TAPFIN EXT'), 'Reason for Review'] = ''

    # delete empty rows in Reason for Review
    df_final = delete_20k(df_final)

    # delete Unnamed columns
    columns_list = [x for x in df_final.columns if 'Unnamed' in x]
    df_final = delete_columns(df_final, columns_list)

    # delete duplicates
    df_final = df_final.drop_duplicates(subset=['Customer Number', 'Total AR'])

    # replace empty cells in Ticker
    df_final.loc[df_final['Ticker'].isnull(),'Ticker'] = 'None'

    # download yahoo data
    df_final = yahoo_scraper_func(df_final)

    # export final file
    export_file(df_final, final_name, path)

# path, ps_name, rmps_name, can_name, us_name, master_name, ps_date_name, final_name
make_final_file('path', 'psbase.xlsx', 'rmbase.xlsx', 
                'can.csv', 'det.csv', 'master.xlsx', 'psdate.xlsx', 'Final File')
