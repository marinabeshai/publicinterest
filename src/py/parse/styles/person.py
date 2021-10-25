from utils import increment_dictionary_in_dictionary, increment_dictionary, add_key_dictionary, make_csv, graph_csv, make_csv_breakdown, path_csv, path_html
import datetime as dt


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions per person.
# trans_per_person_total={'Max': 5, 'Sam': 20, ...}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_person(rows, trans_per_person_total={}):
    for _, transaction in rows:
        trans_per_person_total = increment_dictionary(trans_per_person_total, transaction['senator'])

    filename = "trans_per_person_total"
    key_header = "senator"
    value_header = "number_of_transactions"
    
    make_csv(path_csv, filename, trans_per_person_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions per person per day.
# {'M Person': {year : #_of_transactions_in_year, ... } }
# trans_per_person_breakdown = {}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_person_controlled(rows, trans_per_person_breakdown={}):    
    for _, transaction in rows:
        date = transaction['transaction_date']
        trans_per_person_breakdown = increment_dictionary_in_dictionary(trans_per_person_breakdown, transaction['senator'], date)

    filename = "trans_per_person_breakdown"
    key_header = "senator"
    
    make_csv_breakdown(path_csv, filename, trans_per_person_breakdown, key_header)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
