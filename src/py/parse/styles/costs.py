from utils import increment_dictionary_in_dictionary, increment_dictionary, make_csv, graph_csv, make_csv_breakdown, path_html, path_csv, get_year

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Number of transactions per average cost.
# ticker_total = {'Average_cost': '#_of_transactions'}
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_costs(rows, ticker_total={}):
    for _, transaction in rows:
        date = transaction['transaction_date']
        
        get_price(transaction['ticker'], date, transaction['amount'])
        
        ticker_total = increment_dictionary(ticker_total, transaction['ticker'])

    filename = "ticker_total"
    key_header = "ticker"
    value_header = "number_of_transactions"
    make_csv(path_csv, filename, ticker_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
