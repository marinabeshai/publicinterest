import os
from utils import make_dir, isvalid, get_filename
import csv

# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # @TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def make_csv_breakdown_not_intense(path_csv, filename, d,  key_header):
#     wd = get_filename(path_csv, filename)

#     with open(wd, 'w') as csvfile:

#         filewriter = csv.writer(csvfile)

#         # header row 
#         l = [] 
#         l.append(list(d.keys()))
#         l.append(list(d[  l[0][0] ].keys()))
#         flat_list = [item for sublist in l  for item in sublist]
#         filewriter.writerow(flat_list)


#         for k, inner_dict in d.items():
#             l = [k]
#             for item in inner_dict:
#                 l.append(item)
#             print(l)
#             filewriter.writerow(l)
#     return wd 
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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

def make_csv_base(path_csv, filename, headers, rows):
    wd = get_filename(path_csv, filename)
    with open(wd, 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow(headers)
    
        for row in rows:
            filewriter.writerow(row)
            
    return wd


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def make_csv(path_csv, filename, d, key_header, value_header):
    
#     headers = [key_header, value_header]
#     rows = []
    
#     for k, v in d.items():
#         rows.append([k,v])
    
#     return make_csv_base(path_csv, filename, headers, rows)
    


# # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv(path_csv, filename, d, headers):

    rows = []    

    if type(d) == dict: 
        for k, v in d.items():

            if type(v) is int: 
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
