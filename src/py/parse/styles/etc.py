from utils import increment_dictionary, graph_csv, make_csv, path_csv, path_html

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_act(rows, rows_total={}):
    for _, transaction in rows:
        rows_total = increment_dictionary(rows_total, transaction['type'])
        
    filename = "frequency_of_act"
    key_header = "type"
    value_header = "number_of_transactions"
    make_csv(path_csv, filename, rows_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
     
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_asset_type(rows, type_total={}):
    for _, transaction in rows:
        type_total = increment_dictionary(type_total, transaction['asset_type'])
        
    filename = "frequency_of_asset_type"
    key_header = "asset_type"
    value_header = "number_of_transactions"
    make_csv(path_csv, filename, type_total, key_header, value_header)
    graph_csv(path_csv, path_html, filename, key_header, value_header)
     
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
