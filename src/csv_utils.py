import os
from utils import  isvalid, get_filename
import csv
import pandas as pd 

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_breakdown(path_csv, filename, d,  key_header):
    wd = get_filename(path_csv, filename)

    with open(wd, 'w') as csvfile:

        filewriter = csv.writer(csvfile)
        
        flat_list = set()
        for d2 in d.values():
            for v in d2:
                if isvalid(v):
                    flat_list.add(v)

        flat_list = list(flat_list)
        flat_list.sort()
        flat_list.insert(0, key_header)
        filewriter.writerow(flat_list)
        flat_list.remove(key_header)

        for k, d2 in zip(d.keys(), d.values()):
            row = [""]*len(flat_list)

            row.insert(0, k)

            for y in d2:
                if isvalid(v):
                    row[flat_list.index(y)+1] = d2[y]
                    
            filewriter.writerow(row)
    return wd 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_base(path_csv, filename, headers, rows):
    wd = get_filename(path_csv, filename)
    with open(wd, 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow(headers)
    
        for row in rows:
            filewriter.writerow(row)
            
    return wd

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv(path_csv, filename, d, headers):

    rows = []    

    if type(d) == dict: 
        for k, v in d.items():

            if type(v) is int or type(v) is str: 
                l = [v]
            else:
                l = list(v)
            
            l.insert(0, k)            
            rows.append(l)
    else: 
        for item in d:
            rows.append([item])
            
    return make_csv_base(path_csv, filename, headers, rows)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
