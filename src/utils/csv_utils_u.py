from utils.ptr_utils_u import  isvalid
from utils.dir_utils_u import get_filename
import csv

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_breakdown(path_csv, filename, d,  key_header):
    wd = get_filename(path_csv, filename)

    with open(wd, 'w') as csvfile:

        filewriter = csv.writer(csvfile)

        values = []
        for d2 in d.values():
            for v in d2:
                #  gets rid of nan.
                if isvalid(v) and v not in values:
                    values.append(v)

        values.sort()
        values.insert(0, key_header)
        filewriter.writerow(values)
        values.remove(key_header)

        for k, d2 in zip(d.keys(), d.values()):
            row = [""]*len(values)
            row.insert(0, k)

            # Then for each date, we
            for y in d2:
                if isvalid(y):
                    row[values.index(y) + 1] = d2[y]

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

            # '0QZI.IL': {'2019/09/25': 2},
            elif type(v) is dict:
                l = []
                for k1, v1 in v.items():
                    l.append(k1)
                    l.append(v1)
            else:
                l = list(v)
            
            l.insert(0, k)            
            rows.append(l)
    else: 
        for item in d:
            rows.append([item])
            
    return make_csv_base(path_csv, filename, headers, rows)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
