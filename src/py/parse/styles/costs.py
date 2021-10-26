from utils import increment_dictionary_in_dictionary, increment_dictionary, make_csv, graph_csv, make_csv_breakdown, path_html, path_csv, get_price

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Number of transactions per average cost.
# ticker_total = {'scale_of_shares_roundedby5': '#_of_transactions'}
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_shares(rows, ticker_total={}):
    for _, transaction in rows:
        date = transaction['transaction_date']
        # print(transaction)

        l = get_price(transaction['ticker'], date, transaction['amount'])
        if l:
            ticker_total = increment_dictionary(ticker_total, str(l))

    filename = "frequency_of_shares"
    key_header = "scale_of_shares_rounded_by_5"
    value_header = "number_of_transactions"
    make_csv(path_csv, filename, ticker_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
# # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

