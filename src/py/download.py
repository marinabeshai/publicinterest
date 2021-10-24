import pandas as pd
from datetime import date

# def download():
if __name__ == '__main__':
    
    SENATE_URL = "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.csv"
    HOUSE_URL = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.csv"

    base_file_name = date.today().strftime("%m%d%Y") + '.csv'

    df = pd.read_csv(SENATE_URL)
    df.to_csv("../../curr/senate-" + base_file_name, index=False)

    df = pd.read_csv(HOUSE_URL)
    df.to_csv("../../curr/house-" + base_file_name, index=False)
