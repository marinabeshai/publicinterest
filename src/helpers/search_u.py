# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import utils.constants as constants 
from utils.constants import Unknown
from helpers.official import Official
from polygon import RESTClient
from requests.exceptions import HTTPError
import time
import requests
import wikipedia
from datetime import datetime
from googlesearch import search
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_yfinance(ticker, industry=True):
    assert ticker != '--'
    
    try:
        if '.' in ticker: 
            ticker = ticker[:ticker.find('.')]
        if industry:
            key = "Industry"
        else:
            key = "Sector(s)"
            
        if ticker == "BTC" or ticker == 'DOGE-USD':
            return "cryptocurrency"
        
        if ticker == 'URGO' or ticker == 'WXA.F':
            return None 
        
        if ticker == 'SPDR':
            ticker = 'SPY'
            
        if ticker == 'BLFSD':
            ticker = 'BLFS'
            
        if ticker == 'XER.BE':
            ticker = 'XER2.BE'
            
        if ticker == 'BP PLC':
            ticker = 'BP'
            
        if ticker == 'EBJ':
            ticker = 'ERJ'
        
        # Corner cases.
        if ticker == "ETHE" or ticker == "GBTC" or ticker == "QQQ" or ticker == 'BSTZ' or ticker == 'BMEZ':
            return "Trust"
        
        if ticker == 'VMCXX' or ticker == 'FDRXX' or ticker == 'SNOXX':
            return 'Fund'
        
        if ticker == 'RF$A':
            ticker = 'RF'
            
        if ticker == "RDSA":
            ticker = "RDS-A"
            
        if ticker == 'DGNR':
            ticker = 'CCCS'
            
        # Copied Axon.
        if ticker == "FL4.SG":
            return "Aerospace & Defense" if industry else "Industrials"
        if ticker == "SYY.SG":
            return "Food Distribution" if industry else "Consumer Defensive"
        if ticker == 'NTXFY':
            return 'Financial Services' if industry else 'Banks - Regional'
        if ticker == 'PRSP':
            return 'IT Services' if industry else 'Information Technology'
        if ticker == 'PS':
            return 'Software' if industry else 'Information Technology'


# quite surprising to see international markets 
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
        # print(ticker)
        return None 
        # raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            return None 
            # raise Unknown

        if "429" in str(e):
            time.sleep(60)
            return get_industry(ticker)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            # raise Unknown
            return None 

        if "429" in str(e):
            time.sleep(60)
            return get_sector(ticker)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clean_up_res(res):
    return res[res.find("=")+1:].replace("[", "").replace("]", "").replace("}", "").replace('"', "").replace("{{ubl", "").replace("{{plainlist", "").replace("*", "").replace("{{nowrap|", "").strip()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def parse(d, word, count, s, break_point):
    # Corner Case
    # print(word)
    
    if count == "":
        word = word + " "
    
    index = s.find(word+count)
    # print(index)
    
    if index == -1:
        return d 
    
    where_to_stop = len(word+count) + index
    # print(where_to_stop)
    
    while s[where_to_stop] != break_point:
        where_to_stop += 1

    # print(where_to_stop)
    
    res = s[index+len(word): where_to_stop]
    # print(res) 
    
    if not res and word != "term_start":
        # print(word)
        # print(s)
        raise Exception("Pattern mismatch.")

    else:
        if 'Representatives' in word: 
            word = 'state'
        d[word.strip()] = clean_up_res(res)

    return d
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def go_shopping(name, l, s):
    try:
        d = {}
        
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


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

    try:
        if name == 'Taylor, Nicholas V.':
            name = 'Taylor, Nicholas Van'
        if name == 'Jacobs, Christopher L.':
            name = 'Chris Jacobs'
        if name == 'Pfluger, August L.':
            name = 'Pfluger, August'
        if name == 'Hill, James F.':
            name = 'French Hill'
            
        results = wikipedia.search(name)
        at = 0
        
        s = page(results[at]) 
        if "may refer to" in s: 
            at += 1
            s = page(results[at])  


        while "United States Senator" not in s and "United States representative" not in s and "U.S. representative" not in s and  "United States senator" not in s and "U.S. Representative" not in s and "U.S. House of Representatives" not in s and "United States House of Representatives" not in s:
            at += 1
            s = page(results[at])  
        
        d = go_shopping(name, ["birth_place ", "alma_mater ", "birth_date ", "education "], s)
        d = congress_gov_get(name, d)

        birth_place = d.get("birth_place", None)
        
        education = d.get("alma_mater", None)
        if not education:
            education = d.get("education", None)


        birth_date = d.get("birth_date", None)
        state = d.get("state", None)
        party = d.get("party", None)
        senate = d.get("senate", None)
        house = d.get("house", None)
    
        return Official(name, state, birth_date, birth_place, party, education, senate, house)
        
    except Exception as e:
        print(str(e))
        print(name)
        # print(s)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




def congress_gov_get(name, d):
    # Remove middle initial
    if name[len(name)-1] == ".":
        name = name[:len(name)-3].strip()
        
    # problematic = {"Allen, Richard" : "Allen, Rick", 
    #             "Krishnamoorthi, S." : "Krishnamoorthi, Raja",
    #             "Mcconnell Jr., A." : "McConnell, Mitch",
    #             "Taylor, Nicholas Van" : "Taylor, Van",
    #             "Fallon, Patrick" : "Fallon, Pat",
    #             "Gallagher, Michael" : "Gallagher, Mike",
    #             "Sullivan, Daniel" : "Sullivan, Dan",
    #             "Crapo, Michael" : "Crapo, Mike",
    #             "Hagerty IV, William" : "Hagerty, Bill",
    #             "Duckworth, Ladda" : "Duckworth, Tammy",
    #             "Khanna, Rohit" : "Khanna, Ro",
    #             "Cruz, Rafael" : " Cruz, Ted",
    #             "Wyden, Ronald" : "Wyden, Ron",
    #             "Moore, Felix" : "Moore, Barry",
    #             "Banks, James" : "Banks, Jim",
    #             "Udall, Thomas" : "Udall, Tom",
    #             "Conaway, K." : "Conaway, K. Michael",
    #             "Perdue Jr., David" : "Perdue, david ",
    #             "Crenshaw, Daniel" : "Crenshaw, Dan",
    #             "Arenholz, Ashley" : "Hinson, Ashley",
    #             "Steube, William" : "Steube, W. Gregory",
    #             "Cassidy, William" : "Cassidy, Bill",
    #             "Clay Jr., William" : "Clay, Wm. Lacy",
    #             "Tuberville, Thomas" : "Tuberville, Tommy",
    #             "Kaine, Timothy" : "Kaine, Tim",
    #             "Hagedorn, James" : "Hagedorn, Jim",
    #             "Portman, Robert" : "Portman, Rob" }
    
    # if name in problematic: 
    #     name = problematic[name]

    # htmled_name = name.replace(" ", "%20").replace(",", "%2C")
    # html = 'https://www.congress.gov/search?q=%7B"source"%3A"members"%2C"search"%3A"{name}"%7D'.format(name=htmled_name)
        
    # result = requests.get(html).text
    
    # result = result[result.find('<div><span class="visualIndicator">MEMBER</span></div>') : result.find('<li class="compact" style="display:none">    1.')]
        
    # state = result[result.find('<strong>State:</strong>') : ] 
    # state = state[ : state.find('</span>')]
    # state = state[state.find('<span>') : ].replace("<span>", "")
    
    # senate = house = None 

    # if state: 
    #     party = result[result.find('<strong>Party:</strong>') : ] 
    #     party = party[ : party.find('</span>')]
    #     party = party[party.find('<span>') : ].replace("<span>", "")


    #     served = result[result.find('<strong >Served:</strong>') : ] 
    #     served = served[ : served.find('</span>')]
    #     served = served[served.find('<span>') : ].replace("<span>", "").replace('<ul class="member-served">\n', "").replace("<li>", "")
        
    #     if served.find("Senate: ")  > 0: 
    #         served_temp = served[served.find("Senate: ") + 8 : ] 
    #         senate = served_temp [ : served_temp.find("</li>")]
            
    #     if served.find("House: ")  > 0: 
    #         served_temp = served[served.find("House: ") + 7 : ] 
    #         house = served_temp [ : served_temp.find("</li>")]

        
    # else:
    query = "{} site:congress.gov".format(name)

    result = requests.get(search(query)[0]).text

    party = result[result.find('<th scope="row" class="member_party">Party</th>') : ] 
    party = party[ party.find('<td>') + 4: party.find('</td>')]
    
    # print(result)
    
    senate = house = None
    
    if result.find('<th class="member_chamber">Senate</th>') > 0:
        senate = result[result.find('<th class="member_chamber">Senate</th>') : ] 
        senate = senate[ : senate.find("</td>") ]
        senate = senate[senate.find("<td>") : ]
        state = senate[ : senate.find(",")].replace("<td>", "")
        senate = senate[senate.find("(") : ].replace("(", "").replace(")", "").strip()
    
    if result.find('<th class="member_chamber">House</th>') > 0:
        house = result[result.find('<th class="member_chamber">House</th>') : ] 
        
        while house.find("</td>") > 0: 
            house_temp = house[ : house.find("</td>") ]
            house_temp = house_temp[house_temp.find("<td>") : ]
            state = house_temp[ : house_temp.find(",")].replace("<td>", "")
            house_temp = house_temp[house_temp.find("(") : ].replace("(", "").replace(")", "").strip()
            print("hi")
            print(house)
            

    d['state'] = state
    d['party'] = party
    d['senate'] = senate
    d['house'] = house

    return d 
