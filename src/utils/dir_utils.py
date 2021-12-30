# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd 
import os 
import utils.constants as constants 
from utils.constants import Unknown
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
        url = '../curr/?-10182021.csv'
        if senate:
            path = url.replace("?", constants.SENATE)
        else:
            path = url.replace("?", constants.HOUSE)
            
        csvreader = pd.read_csv(path)
        title = csvreader.columns[8]
        # rows = csvreader.iterrows()
        return title, csvreader
    except Exception:
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# def get_sic_mapping():
#     try:
#         url = '../static/sec_combined.csv'
#         df = pd.read_csv(url)
#         df.reset_index(drop=True, inplace=True)         
#         return df
    
#     except Exception:
#         raise Unknown


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO
# # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
# def get_industry_vx(ticker, api_key='bY4T_AzQ86wiQ6djMEnLEihMmenm4_Jm'):
#     try:
        
#         with RESTClient(api_key) as client:
#             resp = client.reference_ticker_details_vx(ticker).results
#             # industry
#             return resp['sic_description'] 

#     except HTTPError as e:
#         if "404" in str(e):
#             print(ticker)
#             raise Unknown 

#         elif "429" in str(e):
#             time.sleep(60)
#             return get_industry_vx(ticker)
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # TODO
# # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
# def get_sector_vx(ticker, sic_mapping, api_key='bY4T_AzQ86wiQ6djMEnLEihMmenm4_Jm'):
#     try:
        
#         with RESTClient(api_key) as client:
#             resp = client.reference_ticker_details_vx(ticker).results
#             # sector 
#             office =  list(sic_mapping.loc[sic_mapping['SIC_Code'] == int(resp['sic_code']) ].Office)[0]
#             return office[office.find('of')+2:].strip()
        
#     except HTTPError as e:
#         if "404" in str(e):
#             print(ticker)
#             raise Unknown 

#         elif "429" in str(e):
#             time.sleep(60)
#             return get_sector_vx(ticker, sic_mapping)
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
        raise Unknown
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
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------