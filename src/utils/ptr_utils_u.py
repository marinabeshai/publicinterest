from utils.constants_u import DATE_FORMAT
from datetime import date, datetime
import pandas as pd 

def isvalid(s):
    return not pd.isnull(s) and s != "--" and s != "PDF Disclosed Filing" and s != "Unknown"


def within_tax_date(s):
    l = ['01/15/', '04/15/', '06/15/', '09/15/']
    given_date = datetime.strptime(s, '%m/%d/%Y').date()

    for quarter in l:
        tax = quarter + str(given_date.year)[2:]

        check_date = datetime.strptime(tax, '%m/%d/%y').date()

        diff = (check_date - given_date).days
        if diff > 0 and diff <= 14:
            return True

    return False

def format_date(d1):
    return datetime.strptime(d1, "%m/%d/%Y").strftime(DATE_FORMAT)
    


def difference_between_dates(d1, d2):
    d1_obj = datetime.strptime(d1, "%m/%d/%Y")
    d2_obj = datetime.strptime(d2, "%m/%d/%Y")
    return (d1_obj - d2_obj).days


def average_amount(s):
    if "Over" in s:
        # arbitrary 
        return int(gmean([50000001., 150000000.]))

    l = s.replace("$", "").replace(",", "").split(" ")
    l.pop(1)
    l = [float(x) for x in l]

    return int(gmean(l))


def get_year(s):
    return s[6:]
