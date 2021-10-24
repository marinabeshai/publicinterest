import pandas as pd
from datetime import date
import constants

# def download():
if __name__ == '__main__':
    base_file_name = date.today().strftime("%m%d%Y") + '.csv'

    df = pd.read_csv(constants.SENATE_URL)
    df.to_csv("../../curr/senate-" + base_file_name, index=False)

    df = pd.read_csv(constants.HOUSE_URL)
    df.to_csv("../../curr/house-" + base_file_name, index=False)
