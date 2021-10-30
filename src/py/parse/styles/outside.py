from utils import increment_dictionary_in_dictionary, wiki_search
from utils import increment_dictionary, path_csv, make_csv_breakdown

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def frequency_of_amount_by_aff(rows, who_is_what={}):
    affiliations = {}
    for _, transaction in rows:
        person = transaction['senator']
        if person not in affiliations: 
            rep = wiki_search(person)
 
 
            affiliations.update({person : rep.party})
            
        who_is_what = increment_dictionary_in_dictionary(who_is_what, transaction['amount'], affiliations[person])
        
    filename = "frequency_of_amount_by_aff"
    key_header = "amount"

    make_csv_breakdown(path_csv, filename, who_is_what, key_header)
     
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

