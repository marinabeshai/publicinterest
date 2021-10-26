import datetime as dt
import os
import csv
from numpy import e
import pandas as pd
import plotly.express as px
import yfinance as yf
import wikipedia 
import requests
import json
from Rep import Representative

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# https://stackoverflow.com/questions/7638402/how-can-i-get-the-infobox-from-a-wikipedia-article-by-the-mediawiki-api


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def wiki_search(name):
    probable_result_title = wikipedia.search(name)[0]
    htmled_tltle = probable_result_title.replace(" ", "%20")

    resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={person}&rvsection=0'.format(person=htmled_tltle)).json()
        
    page_one = next(iter(resp['query']['pages'].values()))
    revisions = page_one.get('revisions', [])

    l = ["name", "jr/sr", "state", "term_start", "birth_place", "party", "alma_mater", "education"]
    d = {}

    s = list(revisions[0].values())[2]

    for w in l:
        i = s.find(w)
        if i == -1:
            continue
        where_to_stop = len(w) + i 
        while s[where_to_stop] != "|":
            where_to_stop += 1 
            
        res = s[i+len(w): where_to_stop]
        d[w] =  res.replace("=", "").replace("[", "").replace("]", "").strip()
    
    name = d.get("name", None)
    jr = d.get("jr/sr", None)
    state = d.get("state", None)
    term_start = d.get("term_start", None)
    birth_place = d.get("birth_place", None)
    party = d.get("party", None)
    alma_mater = d.get("alma_meter", None)
    education = d.get("education", None)
    
    return Representative(name, jr, state, term_start, birth_place, party, alma_mater, education)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def myround(x, base=5):
    return base * round(x/base)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ohlc_average(row):
    open = float(row['Open'])
    high = float(row['High'])
    low = float(row['Low'])
    close = float(row['Close'])

    return (open + high + low + close)/4
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_shares_scale(average, amount):
    l = amount.split('-')
    nl = []

    for a in l:
        a = a.strip()
        a = a[1:].replace(",", "")

        num_shares = float(a)/average
        nl.append(myround(num_shares))

    return nl
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_price(ticker, date, amount):
    if not isvalid(ticker): 
        return None 
   
    formatted_date = format_transaction_date_df(date)

    start_date, end_date = format_transaction_date_search(date)

    try: 
        # Get the data
        df = yf.download(ticker, start_date, end_date)
        
        if df.empty:
            return None 
                
        for index, row in df.iterrows():
            index = str(index).split(" ")[0]

            if index == formatted_date:
                break

        ohlc_average = get_ohlc_average(row)
        return get_shares_scale(ohlc_average, amount)

    except IndexError:
        print(ticker)
        print("hi")
        print("================================================================")
        exit(1) 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
our_path = '../../../curr/'
path_csv = "results/csv"
path_html = "results/html"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_dir(path):
    cwd = os.getcwd()
    try:
        if path:
            dir = "{cwd}/{path}".format(cwd=cwd, path=path)
            os.makedirs(dir)
    except FileExistsError:
        pass
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def isvalid(s):
    return not pd.isnull(s) and s != "--"
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_breakdown(path_csv, filename, d,  key_header):
    cwd = os.getcwd()
    make_dir(path_csv)

    with open("{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename), 'w') as csvfile:

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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def graph_csv(path_csv, path_html, filename, key_header, value_header, type="normal"):
    cwd = os.getcwd()
    make_dir(path_html)

    name = "{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(
        cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename)

    df = pd.read_csv(name)

    if type != "normal":
        fig = px.scatter(df, x=key_header, y=value_header, title='')
    else:
        fig = px.line(df, x=key_header, y=value_header, title='')

    fig.write_html("{path}{slash}{filename}.html".format(path="{cwd}/{path}".format(
        cwd=cwd, path=path_html), slash=('/' if path_html else None), filename=filename))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv(path_csv, filename, d, key_header, value_header):
    cwd = os.getcwd()
    make_dir(path_csv)

    with open("{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename), 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([key_header, value_header])

        for k, v in zip(d.keys(), d.values()):
            filewriter.writerow([k, v])
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# increment_dictionary( d={'Jack': 1, 'Sam':35}, key='Sam') --> d={'Jack': 1, 'Sam':36}
# increment_dictionary( d={'Jack': 1, 'Sam':35}, key='Percy') --> d={'Jack': 1, 'Sam':35, 'Percy':1}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def increment_dictionary(d, key):
    old = d.get(key, 0)
    d.update({key: (old + 1)})
    return d
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# increment_dictionary( d={'Jack': 1, 'Sam':35}, key='Sam') --> d={'Jack': 1, 'Sam':36}
# increment_dictionary( d={'Jack': 1, 'Sam':35}, key='Percy') --> d={'Jack': 1, 'Sam':35, 'Percy':1}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_key_dictionary(d, key):
    if key in d:
        raise Exception("This isn't possible.")
    d.update({key: 0})
    return d
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# increment_dictionary_in_dictionary(d={'APPL': {'Jack': 1}, 'AMZ': {'Sam': 50, 'Max': 23}}, key:'AMZ', inner_key='Sam') --> d={'APPL': {'Jack': 1}, 'AMZ': {'Sam': 51, 'Max': 23}}
# increment_dictionary_in_dictionary(d={'APPL': {'Jack': 1}, 'AMZ': {'Sam': 50, 'Max': 23}}, key:'AMZ', inner_key='M') --> d={'APPL': {'Jack': 1}, 'AMZ': {'M': 1, 'Sam': 50, 'Max': 23}}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def increment_dictionary_in_dictionary(d, key, inner_key):
    if key in d:
        key_d = d.get(key, 0)

        if key_d == 0:
            raise Exception("This isn't possible.")

        key_d = increment_dictionary(key_d, inner_key)
        d.update({key: key_d})
    else:
        d.update({key: {inner_key: 1}})
    return d
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# format_transaction_date_df('01/07/2011') --> '2011-01-07'
# format_transaction_date_df('1/7/2011') --> '2011-01-07'
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def format_transaction_date_df(s):
    return dt.datetime.strptime(s, "%m/%d/%Y").strftime("%Y-%m-%d")
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# format_transaction_date_search('01/07/2011') -->  '07-01-2011', '17-01-2011'
# format_transaction_date_search('1/7/2011') --> '07-01-2011', '17-01-2011'
# Formatted required by mini_yahoo_finance. We extend the time frame by 10 days because there seems to be a bug of mini_yahoo_finance not accurately capturing dates and times.  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def format_transaction_date_search(s):
    start_date = dt.datetime.strptime(s, "%m/%d/%Y")
    end_date = start_date + dt.timedelta(days=2)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_year(s):
    return s[6:]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
