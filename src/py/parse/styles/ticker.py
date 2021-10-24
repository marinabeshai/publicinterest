from utils import increment_dictionary_in_dictionary, increment_dictionary, make_csv, graph_csv, make_csv_breakdown, path_html, path_csv, get_year

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Number of transactions per ticker.
# ticker_total = {'Ticker': '#_of_transactions'}
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_ticker(rows, ticker_total={}):
    for _, transaction in rows:
        ticker_total = increment_dictionary(ticker_total, transaction['ticker'])

    filename = "ticker_total"
    key_header = "ticker"
    value_header = "number_of_transactions"
    make_csv(path_csv, filename, ticker_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Number of transactions per ticker per person.
# ticker_per_person_breakdown = {'M Person': {ticker : #_of_transactions_in_year, ... } }
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_ticker_breakdown_person(rows, ticker_per_person_breakdown={}):
    for _, transaction in rows:
        ticker_per_person_breakdown = increment_dictionary_in_dictionary(ticker_per_person_breakdown, transaction['senator'], transaction['ticker'])

    filename = "ticker_per_person_breakdown"
    key_header = "ticker"

    make_csv_breakdown(path_csv, filename, ticker_per_person_breakdown, key_header)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Number of transactions per ticker per year.
# trans_per_year_breakdown = {'Ticker': {year : #_of_transactions_in_year, ... } }
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_ticker_breakdown_ticker(rows, trans_per_year_breakdown={}):
    for _, transaction in rows:
        trans_per_year_breakdown = increment_dictionary_in_dictionary(trans_per_year_breakdown, transaction['ticker'], get_year(transaction['transaction_date']))

    filename = "trans_per_year_breakdown"
    key_header = "ticker"
    
    make_csv_breakdown(path_csv, filename, trans_per_year_breakdown, key_header)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
