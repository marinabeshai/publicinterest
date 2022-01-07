# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        url = '../curr/?-01062022.csv'
        if senate:
            path = url.replace("?", constants.SENATE)
        elif house:
            path = url.replace("?", constants.HOUSE)
        else: 
            path_senate = url.replace("?", constants.SENATE)
            csvreader_senate = pd.read_csv(path_senate)

            path_house = url.replace("?", constants.HOUSE)
            csvreader_house = pd.read_csv(path_house)
            
            # csvreader_house.at[8508, constants.TDATE] = '2020-12-29'

            combined_df = pd.concat([csvreader_senate, csvreader_house])
            indexes_to_drop = []

            for i, t in combined_df.iterrows():
                if int(ptr_utils.get_year(ptr_utils.format_date(t[constants.TDATE]))) > 2021:
                    indexes_to_drop.append(i)
                    
            combined_df.drop(combined_df.index[indexes_to_drop], inplace=True)

            return None, combined_df

        csvreader = pd.read_csv(path)
        title = csvreader.columns[8]
        return title, csvreader
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