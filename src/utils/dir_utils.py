# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd 
import os 
import constants as constants 
from constants import EXCEPTION_STRING
from search_u import get_type
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
def get_data(senate=False, house=False):
    assert senate or house
    try: 
        url = '../../curr/?-10182021.csv'
        if senate:
            path = url.replace("?", constants.SENATE)
        else:
            path = url.replace("?", constants.HOUSE)
        csvreader = pd.read_csv(path)
        title = csvreader.columns[8]
        # rows = csvreader.iterrows()
        return title, csvreader
    except Exception:
        print(EXCEPTION_STRING)
        raise() 
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

        base = df.loc[df['ticker'] == ticker]
        if len(base) == 0:
            return get_type(ticker, industry=industry)

        if sector: 
            return list(base[constants.SECTOR])[0]
        
        return list(base[constants.INDUSTRY])[0]
    except Exception:
        print(EXCEPTION_STRING)
        raise() 
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
def get_mapping(errors=False, sector=False, industry=False):
    assert errors or sector or industry
    
    try:
        path = '../../curr/ticker_to_?_mapping_ERRORS.csv'
    
        if sector:
            path = path.replace("?", constants.SECTOR)
        else:
            path = path.replace("?", constants.INDUSTRY)

        if not errors: 
            path = path.replace("_ERRORS", "")
            
            
        return pd.read_csv(path)
    except Exception:
        print(EXCEPTION_STRING)
        raise() 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# dir = makesubdir(constants.path_csv, constants.AMOUNT)
# filename = "most_popular_td_fe_sector"
# x = get_filename(dir, filename)
# x = /Users/marinabeshai/OneDrive/Senior/Thesis/publicinterest/src/utils/../results/csv/amount/most_popular_td_fe_sector.csv
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_filename(path_csv, filename):
    try: 
        cwd = os.getcwd()

        if path_csv:
            dir = "{cwd}/{path}".format(cwd=cwd, path=path_csv)
            try: 
                os.makedirs(dir)
            except FileExistsError:
                pass

        return "{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename)

    except Exception:
        print(EXCEPTION_STRING)
        raise() 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# makesubdir(constants.path_csv, constants.TDATE)
# results/csv/transaction_date
#
# makesubdir(constants.path_csv, constants.AMOUNT)
# ../results/csv/amount
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
def makesubdir(path, last_dir):
    try:
        return "{}/{}".format(path, last_dir)
    except Exception:
        print(EXCEPTION_STRING)
        raise() 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  
if __name__ == '__main__':
    _, df = get_data(senate=True)
    aa = get_mapping(industry=True)

    # sector = search_mapping(aa, "ETHE", ind=True)
    # print(sector)
    # print(get_sector("ETHE"))
    
    for _, k in df.iterrows():
        # print(k['ticker'])
        sector = search_mapping(aa, k["ticker"], industry=True)
       
        if not sector and k['ticker'] != "--" and k['ticker'] != "FL4.SG" and k['ticker'] != "DGNR" and k['ticker'] != 'CTAA': 
            print(k['ticker'], sector)
            # print(g(k['ticker']))
            break 

# FL4.SG no idea what that is 
# dgnr
 