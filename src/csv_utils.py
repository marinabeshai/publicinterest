import os
from utils import make_dir, isvalid, get_filename
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
        # values.insert(1, -1)
        filewriter.writerow(values)
        values.remove(key_header)

        for k, d2 in zip(d.keys(), d.values()):
            row = [""]*(len(values)+1)

            # If there is a dictionary, we begin by adding the congressperson's name to the row.
            if d2:
                row.insert(0, k)

            # Then for each date, we
            for y in d2:
                if isvalid(y):
                    row[values.index(y) + 1] = d2[y]
                # else:
                #     row[values.index(-1) + 1] = d2[y]

            filewriter.writerow(row)
    return wd 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv(path_csv, filename, d, key_header, value_header):

    wd = get_filename(path_csv, filename)
    
    with open(wd, 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([key_header, value_header])

        for k, v in zip(d.keys(), d.values()):
            filewriter.writerow([k, v])
            
    return wd
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_tuples(path_csv, filename, d, key_header, value_header, value_header2):

    wd = get_filename(path_csv, filename)
    
    with open(wd, 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([key_header, value_header, "aff"])

        for k, v in zip(d.keys(), d.values()):
            v1, v2 = v
            filewriter.writerow([k, v1, v2])
            
    return wd
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
