from utils import increment_dictionary_in_dictionary, increment_dictionary, add_key_dictionary, make_csv, graph_csv, make_csv_breakdown
import datetime as dt
path_csv = "results/csv"
path_html = "results/html"

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions for each date. We do not include missing dates.
# trans_per_date_total = {'Date':  #_of_transactions, ...} 
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_dates(rows, trans_per_date_total={}):
    for _, transaction in rows:
        date = transaction['transaction_date']
        trans_per_date_total = increment_dictionary(trans_per_date_total, date)

    filename = "trans_per_date_total"
    key_header = "date"
    value_header = "number_of_transactions"
    make_csv(path_csv, filename, trans_per_date_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of unique transactions for each date by unique w.r.t. congressperson. E.g. if Ted Baker made 40 transactions on 1/1/02 and Sam Wall made 2 transactions on 1/1/02, we 
# conclude that there were two transactions on 1/1/02.
# trans_per_date_control_ppl = {'Date':  {'M Person' : #_of_transactions, 'X Person' : _of_transactions, ...}  } 
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_dates_controlled(rows, trans_per_date_control_ppl={}):
    for _, transaction in rows:
        date = transaction['transaction_date']
        trans_per_date_control_ppl = increment_dictionary_in_dictionary(trans_per_date_control_ppl, date, transaction['senator'])

    d = {}
    for date in trans_per_date_control_ppl:
        d[date] =  len(trans_per_date_control_ppl[date])
                
    
    filename = "trans_per_date_control_ppl"
    key_header = "date"
    value_header = "number_of_transactions_unique"
    make_csv(path_csv, filename, d, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        
        
        
