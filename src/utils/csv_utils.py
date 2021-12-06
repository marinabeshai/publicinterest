# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from utils.ptr_utils import  isvalid
from utils.dir_utils import get_filename
from utils.constants import EXCEPTION_STRING
import csv
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# dir = makesubdir(path_csv, TDATE)
# d = {'Sam' : {'today' : 4 , 'yesterday' : 2424} , 'Jack' : {'today' : 1314 , 'yesterday' : 0} }
# wd = make_csv_breakdown(dir, "rand", d,  "name")
# df = pd.read_csv(wd)
# print(df.head(1))
#   name  today  yesterday
# 0  Sam      4       2424
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_breakdown(path_csv, filename, d,  key_header):
    try:
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
    
    except Exception:
        print(EXCEPTION_STRING)
        raise() 

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# dir = makesubdir(path_csv, TDATE)
# rows =  [['Marshall', 'Mathers']])
# wd = make_csv_base(dir, "filename", ['last_name'], rows)
# df = pd.read_csv(wd)
# print(df.head(5))
#          last_name
# Marshall   Mathers
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_base(path_csv, filename, headers, rows):
    try:
        
        wd = get_filename(path_csv, filename)
        with open(wd, 'w') as csvfile:
            filewriter = csv.writer(csvfile)

            filewriter.writerow(headers)
        
            for row in rows:
                filewriter.writerow(row)
                
        return wd
        
    except Exception:
        print(EXCEPTION_STRING)
        raise() 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# dir = makesubdir(path_csv, TDATE)
# d = {'Marshall' : 'Mathers'}
# wd = make_csv(dir, "filename", d, ['last_name'])
# df = pd.read_csv(wd)
# print(df.head(5))
#          last_name
# Marshall   Mathers
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv(path_csv, filename, d, headers):
    
    try:
        
        rows = []    

        if type(d) == dict: 
            for k, v in d.items():

                if type(v) is int or type(v) is str: 
                    l = [v]

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

    
    except Exception:
        print(EXCEPTION_STRING)
        raise() 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
