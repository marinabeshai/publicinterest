from numpy import inner
import pandas as pd
from os import listdir
from os.path import isfile, join
from styles.outside import frequency_of_amount_by_aff
from styles.costs import frequency_of_shares
from styles.dates import frequency_of_dates, frequency_of_dates_controlled, frequency_of_differences
from styles.person import frequency_of_person, frequency_of_person_controlled
from styles.ticker import frequency_of_ticker_breakdown_person, frequency_of_ticker_breakdown_ticker, frequency_of_ticker
from utils import our_path 
from styles.etc import frequency_of_act, frequency_of_asset_type

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


# for each amount, #oftransactionsperaffiliation

# name", "jr/sr", "state", "term_start", "birth_place", "party", "alma_mater", "education"]
        frequency_of_amount_by_aff(csvreader.iterrows())         
            
        # DATES
        # frequency_of_dates(csvreader.iterrows())            
        # frequency_of_dates_controlled(csvreader.iterrows())
        # frequency_of_differences(csvreader.iterrows())
                                                              
        # # PER PERSON 
        # frequency_of_person(csvreader.iterrows())            
        # frequency_of_person_controlled(csvreader.iterrows())

        # # PER TICKER
        # frequency_of_ticker(csvreader.iterrows())            
        # frequency_of_ticker_breakdown_person(csvreader.iterrows())
        # frequency_of_ticker_breakdown_ticker(csvreader.iterrows())            
        
        # # OF SHARES.
        # frequency_of_shares(csvreader.iterrows())    
    
        # ETC.
        # frequency_of_act(csvreader.iterrows())    
        # frequency_of_asset_type(csvreader.iterrows())


        
    

