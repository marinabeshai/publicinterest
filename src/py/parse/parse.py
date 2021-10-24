import csv
from numpy import inner
import pandas as pd
from os import listdir
from os.path import isfile, join
from styles.costs import frequency_of_shares
from styles.dates import frequency_of_dates, frequency_of_dates_controlled, frequency_of_differences
from styles.person import frequency_of_person, frequency_of_person_controlled
from styles.ticker import frequency_of_ticker_breakdown_person, frequency_of_ticker_breakdown_ticker, frequency_of_ticker
from utils import our_path 

if __name__ == '__main__':
    
    onlyfiles = [f for f in listdir(our_path) if isfile(join(our_path, f))]
    for i in onlyfiles:
        if '.csv' not in i:
            onlyfiles.remove(i)
    
    # for i in onlyfiles:
        # if i includes 'senate': type = 'senator'...
        
    with open(our_path+onlyfiles[0]) as f:
        our_path = onlyfiles[0][:onlyfiles[0].find(".")]
        csvreader = pd.read_csv(f)
        rows = csvreader.iterrows()

        # DATES
        # frequency_of_dates(rows)            
        # frequency_of_dates_controlled(rows)
        # frequency_of_differences(rows)
                                                              
        # PER PERSON 
        # frequency_of_person(rows)            
        # frequency_of_person_controlled(rows)

        # PER TICKER
        # frequency_of_ticker(rows)            
        # frequency_of_ticker_breakdown_person(rows)
        # frequency_of_ticker_breakdown_ticker(csvreader.iterrows())            
        
        # BUG AT BELOW. 
        frequency_of_shares(rows)
        # get # of shares
        # print(, transaction['amount'])
        # make_csv(path, "trans_per_date_total", trans_per_date_total)

        # transaction['disclosure_date']
        # transaction['asset_description']
        # transaction['asset_type']
        # transaction['type']
        # transaction['comment']
        # transaction['ptr_link']