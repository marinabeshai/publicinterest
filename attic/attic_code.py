#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Finds missing dates in a dictionary (assuming the dates are keys) and adds it into the dictionary with value of 0.
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_missing_dates(dict):
#     l = list(dict.keys())
#     today = dt.date.today()

#     while l:
#         start_date = l.pop()
#         #     # if start_date.weekday() > 4:
#         #     print("Weekend")

#         start_date_obj = dt.datetime.strptime(start_date, "%m/%d/%Y") 
        
#         try: 
#             next_date_obj = (start_date_obj + dt.timedelta(days=1))
#             next_date_str = next_date_obj.strftime("%m/%d/%Y")
#         except OverflowError:
#             continue 
        
#         if dt.date(next_date_obj.year, next_date_obj.month, next_date_obj.day) > today: 
#             continue 
        
#         if next_date_str not in dict:
#             dict = add_key_dictionary(dict, next_date_str)
#             l.append(next_date_str)
            
# # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         from utils import increment_dictionary, sort_dictionary_by_values, path_csv
# from csv_utils import make_csv_tuples
# import plotly.express as px
# from wiki import wiki_search

# def num_of_trans_per_person_w_aff(trans_per_person_res, d={}, aff={}):
#     res = {}
#     for k, v in trans_per_person_res.items():
#         if k not in aff:
#             aff[k] = wiki_search(k)
#         res[k] = (v, aff[k].get_party(), aff[k].get_num_of_years())
        
#     filename = "num_of_trans_per_person_with_aff"
#     key_header = title
#     value_header = "number_of_transactions"
#     value_header2 = "affiliation"
#     value_header3 = "number of years in congress"

    
#     wd = make_csv_tuples(path_csv, filename, res, key_header, value_header, value_header2, value_header3)
#     df = pd.read_csv(wd)
#                 #  hover_name=value_header , log_x=True, 
#     fig = px.scatter(df, x=value_header3, y=value_header, 
# 	         color=value_header2, size=value_header, size_max=60)
#     fig.show()

#     return d 

# trans_per_person_res = num_of_trans_per_person_w_aff(trans_per_person_res)



# def update_csv(old_csv_path, new_rows, path_csv, filename, headers):
#     csvreader = pd.read_csv(old_csv_path)
#     rows = csvreader.iterrows()
#     l = []
#     for _, transaction in rows:        
#         l.append([transaction['ticker'], transaction['industry']])


#     print(l)
#     for (k, v) in new_rows.items():
#         l.append([k, v])
        
#     print(l)
        
#     return make_csv_base(path_csv, filename,headers, l)
    
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def make_csv(path_csv, filename, d, key_header, value_header):
    
#     headers = [key_header, value_header]
#     rows = []
    
#     for k, v in d.items():
#         rows.append([k,v])
    
#     return make_csv_base(path_csv, filename, headers, rows)
    
    
    
    # # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # @TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def make_csv_breakdown_not_intense(path_csv, filename, d,  key_header):
#     wd = get_filename(path_csv, filename)

#     with open(wd, 'w') as csvfile:

#         filewriter = csv.writer(csvfile)

#         # header row 
#         l = [] 
#         l.append(list(d.keys()))
#         l.append(list(d[  l[0][0] ].keys()))
#         flat_list = [item for sublist in l  for item in sublist]
#         filewriter.writerow(flat_list)


#         for k, inner_dict in d.items():
#             l = [k]
#             for item in inner_dict:
#                 l.append(item)
#             print(l)
#             filewriter.writerow(l)
#     return wd 
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


from utils import path_csv, get_data, isvalid
from csv_utils import make_csv
from search import get_industry
import pandas as pd 

def get_industry_mapping():
    _, rows = get_data()
    tickers = set()
    
    for _, transaction in rows:
        ticker = transaction['ticker']
        if isvalid(ticker):
            tickers.add(ticker)
    
    # print("Finished Tickers")
    print(len(tickers))
        
    results = {}
    errors = {}
    i = 0 
    for ticker in tickers:     
        print(i)
        i += 1        
        p = get_industry(ticker)     
        if not p:
            errors[ticker] = ""    
        else: 
            results[ticker] = p  
            
    print("Finished Errors and Results")

    filename = "ticker_to_industry_mapping"
    key_header = "ticker"
    value_header = "industry"

    wd = make_csv(path_csv, filename, results, [key_header, value_header])
    df = pd.read_csv(wd)
    print(df.head(5))
    
    
    filename = "ticker_to_industry_mapping_ERRORS"
    key_header = "ticker"
    value_header = ""

    wd = make_csv(path_csv, filename, errors, [key_header, value_header])
    df = pd.read_csv(wd)
    print(df.head(5))
    
    return 
    
    
get_industry_mapping()