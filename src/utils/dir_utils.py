# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from importlib_metadata import csv
import pandas as pd 
import os 
import utils.constants as constants 
from utils.constants import Unknown
import utils.ptr_utils as ptr_utils
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# x, y = get_data(senate=True)
# x = senator
# for i in y:
#   print(i)
#   break 
# i =   (0, transaction_date                                            09/30/2021
#       owner                                                            Joint
#       ticker                                                              PG
#       asset_description      Procter &amp; Gamble Company (The) Common Stock
#       asset_type                                                       Stock
#       type                                                          Purchase
#       amount                                                $1,001 - $15,000
#       comment                                                             --
#       senator                                            Thomas H Tuberville
#       ptr_link             https://efdsearch.senate.gov/search/view/ptr/a...
#       disclosure_date                                             10/15/2021
#       Name: 0, dtype: object)
# 
# x, y = get_data(house=True)
# x = representative
# i =   (0, disclosure_year                                                        2021
#       disclosure_date                                                  10/04/2021
#       transaction_date                                                 2021-09-27
#       owner                                                                 joint
#       ticker                                                                   BP
#       asset_description                                                    BP plc
#       type                                                               purchase
#       amount                                                     $1,001 - $15,000
#       representative                                           Hon. Virginia Foxx
#       district                                                               NC05
#       ptr_link                  https://disclosures-clerk.house.gov/public_dis...
#       cap_gains_over_200_usd                                                False
#       Name: 0, dtype: object)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_data(senate=False, house=False, combined=False):
    assert senate or house or combined 
    try: 
        url = '../curr/?-01282022.csv'
        if senate:
            path = url.replace("?", constants.SENATE)
            csvreader = pd.read_csv(path)
       
        elif house:
            path = url.replace("?", constants.HOUSE)
            csvreader = pd.read_csv(path)
      
        else: 
            path_senate = url.replace("?", constants.SENATE)
            csvreader_senate = pd.read_csv(path_senate)

            path_house = url.replace("?", constants.HOUSE)
            csvreader_house = pd.read_csv(path_house)
            
            csvreader = pd.concat([csvreader_senate, csvreader_house], ignore_index=True)


        indexes_to_drop = []

        for i, t in csvreader.iterrows():
            if int(ptr_utils.get_year(ptr_utils.format_date(t[constants.TDATE]))) > 2021:
                indexes_to_drop.append(i)
                
        csvreader.drop(csvreader.index[indexes_to_drop], inplace=True)
        
        for i,t in csvreader.iterrows():
            csvreader.at[i, constants.TDATE] = ptr_utils.format_date(t[constants.TDATE])
            csvreader.at[i, constants.DDATE] = ptr_utils.format_date(t[constants.DDATE])
            
            if t[constants.TYPE] == 'purchase' or t[constants.TYPE] == 'exchange':
                csvreader.at[i, constants.TYPE] = t[constants.TYPE].capitalize()
            elif t[constants.TYPE] == 'sale_full':
                csvreader.at[i, constants.TYPE] = 'Sale (Full)'
            elif t[constants.TYPE] == 'sale_partial':
                csvreader.at[i, constants.TYPE] = 'Sale (Partial)'

        return csvreader.columns[8], csvreader

    except Exception:
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def combined_dfs():
    try: 
        _, input_df_senate = get_data(senate=True)
        _, input_df_house = get_data(house=True)
        combined_input = pd.concat([input_df_senate, input_df_house])
        combined_input.to_csv("combined.csv", sep='\t')
        return 
    
    except Exception:
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# dir = makesubdir(constants.path_csv, constants.AMOUNT)
# filename = "most_popular_td_fe_sector"
# x = get_filename(dir, filename)
# x = /Users/marinabeshai/OneDrive/Senior/Thesis/publicinterest/src/utils/../results/csv/amount/most_popular_td_fe_sector.csv
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_filename(path_csv, filename, ending='csv'):
    try: 
        cwd = os.getcwd()

        if path_csv:
            dir = "{cwd}/{path}".format(cwd=cwd, path=path_csv)
            try: 
                os.makedirs(dir)
            except FileExistsError:
                pass

        return "{path}{slash}{filename}.{ending}".format(path="{cwd}/{path}".format(cwd=cwd, path=path_csv), ending=ending, slash=('/' if path_csv else None), filename=filename)

    except Exception:
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# makesubdir(constants.path_csv, constants.TDATE)
# results/csv/transaction_date
#
# makesubdir(constants.path_csv, constants.AMOUNT)
# ../results/csv/amount
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def makesubdir(path, last_dir):
    try:
        return "{}/{}".format(path, last_dir)
    except Exception:
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# df = get_mapping(errors=False, sector=True, industry=False)
# ticker = "AAPL"
# x = search_mapping(df, ticker, sector=True, industry=False)
# Technology
#
# df = get_mapping(errors=False, sector=False, industry=True)
# ticker = "AAPL"
# x = search_mapping(df, ticker, sector=False, industry=True)
# x = Consumer Electronics
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
def search_mapping(df, ticker, sector=False, industry=False):
    try: 
        assert sector or industry
        if sector:
            assert df.columns[1] == constants.SECTOR
        elif industry:
            assert df.columns[1] == constants.INDUSTRY

        base = df.loc[df[constants.TICKER] == ticker]

        if sector: 
            return list(base[constants.SECTOR])[0]
        
        return list(base[constants.INDUSTRY])[0]
    except Exception:
        raise Unknown 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# x = get_mapping(errors=True, sector=False, industry=False).head(1) 
#         ticker
# DE     NaN
#    
# x = get_mapping(errors=False, sector=True, industry=False).head(1)
#  ticker      sector
# 0      A  Healthcare

# x = get_mapping(errors=False, sector=False, industry=True).head(1)
#     ticker                        industry
# 0  0QZI.IL  Internet Content & Information# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_mapping(sector=False, industry=False):
    assert sector or industry
    
    try:
        path = '../curr/ticker_to_?_mapping.csv'
    
        if sector:
            path = path.replace("?", constants.SECTOR)
        else:
            path = path.replace("?", constants.INDUSTRY)
            
        return pd.read_csv(path)
    except Exception:
        raise Unknown 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def func(d):
    rows = []
    
    for name in d:
        temp = name + "\n"
        for committee in d[name]:
            temp += "\t\t\t" + committee + "\t\t\t" + str(d[name][committee])
        temp += "\n\n"
        rows.append(temp)
        rows.append("\n\n\n\n")
    return rows 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def write_to_file(path_csv, filename, d,  headers, func=func):
    wd = get_filename(path_csv, filename, ending='txt')
    with open(wd, 'w') as f:
        
        rows = []
        for little_d in d: 
            rows.append(func(little_d))

        for r in rows:
            for x in r: 
                f.write(x)
        f.close()
        
    return wd 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
