from numpy import inner
import pandas as pd
from os import listdir
from os.path import isfile, join
from mini_yahoo_finance import get_stock_df
from dates import frequency_of_dates,frequency_of_dates_controlled
from per_person import frequency_of_person, frequency_of_person_controlled
from utils import our_path 

if __name__ == '__main__':
    
    onlyfiles = [f for f in listdir(our_path) if isfile(join(our_path, f))]
    for i in onlyfiles:
        if '.csv' not in i:
            onlyfiles.remove(i)
    
    with open(our_path+onlyfiles[0]) as f:
        our_path = onlyfiles[0][:onlyfiles[0].find(".")]
        csvreader = pd.read_csv(f)

        # DATES
        frequency_of_dates(csvreader.iterrows())            
        frequency_of_dates_controlled(csvreader.iterrows())
                                                        
                                                              
        # PER PERSON 
        frequency_of_person(csvreader.iterrows())            
        frequency_of_person_controlled(csvreader.iterrows())



        # {'M Person': #_of_transactions, 'X Person': _of_transactions, ...}
        # trans_per_person_total = {'Senator': '#_of_transactions'}
        
        
    





        # {'M Person': {ticker : #_of_transactions_in_year, ... } }
        # ticker_per_person_breakdown = {}

        # {'Ticker': #_of_transactions, ...}
        # ticker_total = {'Ticker': '#_of_transactions'}

        # {'Ticker': {year : #_of_transactions_in_year, ... } }
        # trans_per_year_breakdown = {}

            
            
            # print(trans_per_date_total)
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
            # print(get_price(transaction['ticker'], date, transaction['amount']), transaction['amount'])

            # make_csv(path, "trans_per_date_total", trans_per_date_total)

            

            # transaction['asset_type']
            # transaction['type']
            # transaction['comment']
            # transaction['ptr_link']

            # difference between transaction date and disclosure date
            # transaction['disclosure_date']


    # make_csv(path, "trans_per_date_total", trans_per_date_total)
    # get_missing_dates(trans_per_date_total)
                    # transaction['asset_description']
