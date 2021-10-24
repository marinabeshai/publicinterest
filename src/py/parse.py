import csv
from numpy import inner
import pandas as pd
import os 
from os import listdir
from os.path import isfile, join
import datetime as dt 
from mini_yahoo_finance import get_stock_df

def isvalid(s):
    return not pd.isnull(s)

def get_ohlc_average(row):
    open = float(row['Open'])
    high = float(row['High'])
    low = float(row['Low'])
    close = float(row['Close'])
    return (open + high + low + close)/4
    

def get_shares_scale(average, amount):   
    l = amount.split('-')
    nl = []

    for a in l: 
        a = a.strip()
        a = a[1:].replace(",", "")
        
        num_shares =  (float(a)/average)
        nl.append(float(str(round(num_shares, 2))))

    return nl 

def format_transaction_date_df(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").strftime("%Y-%m-%d")

def format_transaction_date_search(s):
    # 1/2/13 --> YYYY-MM-DD
    start_date = dt.datetime.strptime(s, "%m/%d/%Y")
    end_date = start_date + dt.timedelta(days=10)
    return start_date.strftime("%d-%m-%Y"), end_date.strftime("%d-%m-%Y")

def get_price(ticker, date, amount):
    formatted_date = format_transaction_date_df(date)

    try: 
        start_date, end_date = format_transaction_date_search(date)

        df = get_stock_df(ticker,
            start_date,
            end_date=end_date,
            interval='1d',
            max_retries=3)

        for _, row in df.iterrows():            
            if row['Date'] == formatted_date: 
                break 
        
        ohlc_average = get_ohlc_average(row)
        return get_shares_scale(ohlc_average, amount)

    except Exception as e:
        print(e) 
        return None 

    
def increment_dictionary(d, key):
    old = d.get(key, 0)
    d.update({key : (old + 1)})
    return d 

def increment_dictionary_in_dictionary(d, key, inner_key):
    if key in d:
        year_d = d.get(key, 0)
        year_d = increment_dictionary(year_d, inner_key)
        d.update({key : year_d})
    else: 
        d.update({key : {inner_key : 1}})
    return d 

def get_year(s):
    return s[6:]

def make_dir(path):
    cwd = os.getcwd()
    try:
        if path:
            dir = "{cwd}/{path}".format(cwd=cwd, path=path)
            os.mkdir(dir)
    except FileExistsError:
        pass  

# For making the breakdown of transaction count for each senator by year.
def make_csv_breakdown(path, filename, d):
    cwd = os.getcwd()
    make_dir(path)

    with open("{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path), slash=('/' if path else None), filename=filename), 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        inner_key = []
        for d2 in  d.values():
            for y in d2:
                #  gets rid of nan.
                if isvalid(y) and y not in inner_key: 
                    inner_key.append(y)

        inner_key.sort()
        inner_key.insert(0, "Senator")
        filewriter.writerow(inner_key)
        inner_key.remove("Senator")

        for k,d2 in zip(d.keys(), d.values()):
            row = [""]*(len(inner_key)+1)
            
            if d2:
                row.insert(0, k)

            for y in d2:
                if isvalid(y):
                    row[inner_key.index(y) + 1] = d2[y]

            filewriter.writerow(row)

def make_csv(path, filename, d):
    cwd = os.getcwd()
    make_dir(path)

    with open("{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path), slash=('/' if path else None), filename=filename), 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        for k,v in zip(d.keys(), d.values()):
            filewriter.writerow([k,v])


if __name__ == '__main__':
    def valid_entry(s):
        return not pd.isnull(s) and s != "--"
    
    path = '../../curr/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    

    
    with open(path+onlyfiles[0]) as f:
        path = onlyfiles[0][:onlyfiles[0].find(".")]
        
        csvreader = pd.read_csv(f)
        
        # {'M Person': #_of_transactions, 'X Person': _of_transactions, ...}
        # trans_per_person_total = {'Senator': '#_of_transactions'}
        
        # {'M Person': {year : #_of_transactions_in_year, ... } }
        # trans_per_person_breakdown = {}

        # {'M Person': {ticker : #_of_transactions_in_year, ... } }
        # ticker_per_person_breakdown = {}

        # # {'Ticker': #_of_transactions, ...}
        # ticker_total = {'Ticker': '#_of_transactions'}

        # # {'Ticker': {year : #_of_transactions_in_year, ... } }
        # trans_per_year_breakdown = {}


        										
        for _, transaction in csvreader.iterrows():
            date = transaction['transaction_date']

            # trans_per_person_total = increment_dictionary(trans_per_person_total, transaction['senator'])
            # make_csv(path, "trans_per_person_total", trans_per_person_total)

            # trans_per_person_breakdown = increment_dictionary_in_dictionary(trans_per_person_breakdown, transaction['senator'], get_year(date))
            # make_csv_breakdown(path, "trans_per_person_breakdown", trans_per_person_breakdown)

            # ticker_per_person_breakdown = increment_dictionary_in_dictionary(ticker_per_person_breakdown, transaction['senator'], transaction['ticker'])
            # make_csv_breakdown(path, "ticker_per_person_breakdown", ticker_per_person_breakdown)

            # ticker_total = increment_dictionary(ticker_total, transaction['ticker'])
            # make_csv(path, "ticker_total", ticker_total)

            # trans_per_year_breakdown = increment_dictionary_in_dictionary(trans_per_year_breakdown, transaction['ticker'], get_year(date))
            # make_csv_breakdown(path, "trans_per_year_breakdown", trans_per_year_breakdown)

            # get # of shares
            print(get_price(transaction['ticker'], date, transaction['amount']), transaction['amount'])

            # transaction['asset_type']
            # transaction['type']
            # transaction['comment']
            # transaction['ptr_link']

            # difference between transaction date and disclosure date
            # transaction['disclosure_date']




                    # transaction['asset_description']
