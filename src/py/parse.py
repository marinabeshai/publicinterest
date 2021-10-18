import csv
from numpy import inner
import pandas as pd
from os import listdir
from os.path import isfile, join


if __name__ == '__main__':
    def valid_entry(s):
        return not pd.isnull(s) and s != "--"
    
    path = '../../curr/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    
    def increment_dictionary(dict, key):
        if key in dict:
            dict[key] += 1 
        else: 
            dict[key] = 1 
        return dict 

    def increment_dictionary_in_dictionary(dict, key, inner_key):
        if key in dict:
            if inner_key in dict[key]:
                dict[key][inner_key] += 1 
            else: 
                dict[key][inner_key] = 1 
        else: 
            dict[key] = {inner_key : 1}
        return dict 

    def get_year(s):
        
        return s[6:]
    
    with open(path+onlyfiles[0]) as f:
        
        csvreader = pd.read_csv(f)
        
        # {'M Person': #_of_transactions, 'X Person': _of_transactions, ...}
        per_person_total = {}
        
        # {'M Person': {year : #_of_transactions_in_year, ... } }
        per_person_breakdown = {}
        										
        for _, transaction in csvreader.iterrows():
            # transaction['owner']
            date = transaction['transaction_date']

            per_person_total = increment_dictionary(per_person_total, transaction['senator'])
            per_person_breakdown = increment_dictionary_in_dictionary(per_person_breakdown, transaction['senator'], get_year(date))

    
            # transaction['ticker']
            # transaction['asset_description']
            # transaction['asset_type']
            # transaction['type']
            # transaction['amount']
            # transaction['comment']
            
                
                
            # transaction['ptr_link']
            # transaction['disclosure_date']


            # break     
            # if valid_entry(i): print(i)
        
        
    
    print(per_person_breakdown)

        