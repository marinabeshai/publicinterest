from utils import increment_dictionary, add_key_dictionary, make_csv, our_path, graph_csv
import datetime as dt

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions for each date. @TODO MAKE SURE MISSING DATES ARE 0  
# {'Date':  #_of_transactions, ...} 
# trans_per_date_total = {}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_dates(rows, trans_per_date_total={}):
    for _, transaction in rows:
        date = transaction['transaction_date']
        trans_per_date_total = increment_dictionary(trans_per_date_total, date)

    path = "results"
    filename = "trans_per_date_total"
    key_header = "date"
    value_header = "number_of_transactions"
    make_csv(path, filename, trans_per_date_total, key_header, value_header)
    graph_csv(path, filename, key_header, value_header)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO 
# They can transact on the weekends. 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_missing_dates(dict):
    l = list(dict.keys())
    today = dt.date.today()

    while l:
        start_date = l.pop()
        #     # if start_date.weekday() > 4:
        #     print("Weekend")

        start_date_obj = dt.datetime.strptime(start_date, "%m/%d/%Y") 
        
        try: 
            next_date_obj = (start_date_obj + dt.timedelta(days=1))
            next_date_str = next_date_obj.strftime("%m/%d/%Y")
        except OverflowError:
            continue 
        
        if dt.date(next_date_obj.year, next_date_obj.month, next_date_obj.day) > today: 
            continue 
        
        if next_date_str not in dict:
            dict = add_key_dictionary(dict, next_date_str)
            l.append(next_date_str)
            
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        
        
