# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import utils.constants as constants 
from utils.constants import Unknown
from polygon import RESTClient
import time
from requests.exceptions import HTTPError
import requests
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_yfinance(ticker, industry=True):
    assert ticker != '--'
    
    try:
        
        if industry:
            key = "Industry"
        else:
            key = "Sector(s)"
            
        if ticker == "BTC":
            return "cryptocurrency"
        
        # Corner cases.
        if ticker == "ETHE" or ticker == "GBTC" or ticker == "QQQ":
            return "Trust"
        
        if ticker == "RDSA":
            ticker = "RDS-A"
            
        url = "https://finance.yahoo.com/quote/TICKER/profile?p=TICKER".replace("TICKER", str(ticker))
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'

        headers = {'User-Agent': agent}

        response = requests.get(url, headers=headers)
        
        if "Fund Family</span>" in response.text:
            return "Fund"
        
        i = 0         
        while response.text.find(key, i) > 0: 
            i = response.text.find(key, i) + 1
            if i == -1: 
                break 
            
            key_line = response.text[response.text.find(key):response.text.find(key)+300]
            if "reactid" in key_line:
                if ">" not in key_line:
                    continue
                key_line = key_line.split(">")
                return key_line[4].split("<")[0].replace("&amp;", "&")
            
            elif "Fw(600)" in key_line:
                key_line = key_line[key_line.find('Fw(600)') : ].split(">")
                return key_line[1].split("<")[0].replace("&amp;", "&")                
                        
        if key == "Sector(s)":
            key = '<a href="https://finance.yahoo.com/sector/'

            if response.text.find(key) > 0:
                key_line = response.text[response.text.find(key):response.text.find(key)+300]
                key_line = key_line.split(">")   
                result = key_line[1].replace("</a", "")                
                key_line = key_line[0]
                key_line = key_line[ key_line.find("data-symbol=") : ]                
                key_line = key_line[: key_line.find(" ")]
                key_line = key_line[key_line.find('"') : ].replace('"', "")
                
                key_line = list(key_line)
                for letter in ticker:
                    if letter in key_line:
                        key_line.remove(letter)
                    else:
                        return None 
                return result

        return None 
    
    except Exception:
        print(ticker)
        raise Unknown
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
def get_industry(ticker):
    try:
        
        with RESTClient(constants.api_key) as client:
            resp = client.reference_ticker_details(ticker)
            return resp.industry if resp.industry != "" else get_yfinance(ticker, industry=True)

    except HTTPError as e:
        if "404" in str(e):
            res = get_yfinance(ticker, industry=True)
            if res:
                return res
            raise Unknown

        if "429" in str(e):
            time.sleep(60)
            return get_industry(ticker)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
def get_sector(ticker):
    try:
        
        with RESTClient(constants.api_key) as client:
            resp = client.reference_ticker_details(ticker)
            return resp.sector if resp.sector != "" else get_yfinance(ticker, industry=False)
        
    except HTTPError as e:
        if "404" in str(e):
            res = get_yfinance(ticker, industry=False)
            if res:
                return res
            raise Unknown

        if "429" in str(e):
            time.sleep(60)
            return get_sector(ticker)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clean_up_res(res):
    return res[res.find("=")+1:].replace("[", "").replace("]", "").replace("}", "").replace('"', "").replace("{{ubl", "").replace("{{plainlist", "").replace("*", "").replace("{{nowrap|", "").strip()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def parse(d, word, count, s, break_point):
    # Corner Case
    if count == "":
        word = word + " "
    
    index = s.find(word+count)
    
    if index == -1:
        return d 
    where_to_stop = len(word+count) + index

    while s[where_to_stop] != break_point:
        where_to_stop += 1

    res = s[index+len(word): where_to_stop]

    if not res and word != "term_start":
        print(word)
        print(s)
        raise Exception("Pattern mismatch.")

    else:
        d[word.strip()] = clean_up_res(res)

    return d
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def terms(s):
    d = {}

    jr = "jr/sr"
    term_start = "term_start"
    term_end = "term_end"
    state = "state"
    count = ""

    if s[s.find(jr) + len(jr): s.find(jr) + len(jr)+1].isdigit():
        count = s[s.find(jr) + len(jr): s.find(jr) + len(jr)+1]

    d = parse(d, jr, count, s, "|")
    d = parse(d, term_start, count, s, "|")
    d = parse(d, term_end, count, s, "|")
    d = parse(d, state, count, s, "|")

    return d
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def go_shopping(name, l, s, d):
    try:

        while l:
            w = l.pop()                
            i = s.find(w)
            

            # Corner Case
            if "state " == w:
                if s.find("enator from") > 0:
                    leftover = s[s.find("enator from") - 1:]
                    d[w.strip()] = leftover[leftover.find(
                        "from")+5:leftover.find("}}")]
                    continue
                if s.find("state ") == -1 and s.find("state1") > 0:
                    l.append("state1")
                    continue

            if i == -1:
                continue

            else:
                where_to_stop = len(w) + i

                if w == "education ":
                    where_to_stop = s.find("=", where_to_stop) + 1 
                                        
                    if s.find("=", where_to_stop) < s.find("'''", where_to_stop) and  s.find("=", where_to_stop) != -1:
                        where_to_stop =  s.find("=", where_to_stop)
                    else:
                        where_to_stop =  s.find("'''", where_to_stop)

                    
                # Corner case
                elif w == "birth_date ":
                    where_to_stop = s.find("}", where_to_stop)


                elif w == "alma_mater " or w == "birth_place ":
                    where_to_stop = s.find("\n", where_to_stop)

        
                else:
                    where_to_stop = s.find("|", where_to_stop)

                res = s[i+len(w): where_to_stop]           

                # Corner Case
                if w == "birth_date ":
                    res = res[res.find("|") + 1:].replace("|", "/")
                    
                    if not res[0].isdigit():
                        while not res[0].isdigit():
                            res = res[1:]
                        d[w.strip()] = datetime.strptime(res,  '%Y/%m/%d').strftime("%Y/%m/%d")
                        
                    if "-" in res: 
                        d[w.strip()] = datetime.strptime(res,  '%Y-%m-%d').strftime("%Y/%m/%d")
                        
                    elif "age" in res: 
                        # mf=y/1952/12/01
                        d[w.strip()] = datetime.strptime(res[res.find("age")+4:],  '%Y/%m/%d').strftime("%Y/%m/%d")
                        
                    else: 
                        d[w.strip()] = datetime.strptime(res,  '%Y/%m/%d').strftime("%Y/%m/%d")



                else:
                    d[w.strip()] = clean_up_res(res)

        return d

    except Exception as e:
        print(e)
        print(name)
        # return {}
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def page(probable_result_title):
    htmled_tltle = probable_result_title.replace(" ", "%20")

    resp = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={person}&rvsection=0'.format(person=htmled_tltle)).json()

    page_one = next(iter(resp['query']['pages'].values()))
    revisions = page_one.get('revisions', [])

    s = list(revisions[0].values())[2]
    return s
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# https://stackoverflow.com/questions/7638402/how-can-i-get-the-infobox-from-a-wikipedia-article-by-the-mediawiki-api
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def wiki_search(name):

    results = wikipedia.search(name)
    at = 0
    s = ""
    
    while "United States Senator" not in s:
        s = page(results[at])
        at += 1
            
        
    d = terms(s)
    

    d = go_shopping(name, ["birth_place ", "party ", "alma_mater ", "birth_date ", "education "], s, d)


    jr = d.get("jr/sr", None)
    birth_place = d.get("birth_place", None)
    party = d.get("party", None)
    alma_mater = d.get("alma_mater", None)
    education = d.get("education", None)
    birth_date = d.get("birth_date", None)
    term_start = d.get("term_start", None)
    term_end = d.get("term_end", None)
    state = d.get("state", None)

    x = Official(name, jr, state, term_start, term_end,
                 birth_date, birth_place, party, alma_mater, education)

    return x
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
