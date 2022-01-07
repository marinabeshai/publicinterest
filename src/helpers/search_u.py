# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import utils.constants as constants 
import utils.dict_utils as dict_utils 
from helpers.official import Official
from helpers.congress import Congress
from polygon import RESTClient
from requests.exceptions import HTTPError
import time
import requests
import wikipedia
from datetime import datetime
from googlesearch import search
import itertools

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # @TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_yfinance(ticker, industry=True):
#     assert ticker != '--'
    
#     try:
#         if '.' in ticker: 
#             ticker = ticker[:ticker.find('.')]
#         if industry:
#             key = "Industry"
#         else:
#             key = "Sector(s)"
            
#         if ticker == "BTC" or ticker == 'DOGE-USD':
#             return "cryptocurrency"
        
#         if ticker == 'URGO' or ticker == 'WXA.F':
#             return None 
        
#         if ticker == 'SPDR':
#             ticker = 'SPY'
            
#         if ticker == 'BLFSD':
#             ticker = 'BLFS'
            
#         if ticker == 'XER.BE':
#             ticker = 'XER2.BE'
            
#         if ticker == 'BP PLC':
#             ticker = 'BP'
            
#         if ticker == 'EBJ':
#             ticker = 'ERJ'
        
#         # Corner cases.
#         if ticker == "ETHE" or ticker == "GBTC" or ticker == "QQQ" or ticker == 'BSTZ' or ticker == 'BMEZ':
#             return "Trust"
        
#         if ticker == 'VMCXX' or ticker == 'FDRXX' or ticker == 'SNOXX':
#             return 'Fund'
        
#         if ticker == 'RF$A':
#             ticker = 'RF'
            
#         if ticker == "RDSA":
#             ticker = "RDS-A"
            
#         if ticker == 'DGNR':
#             ticker = 'CCCS'
            
#         # Copied Axon.
#         if ticker == "FL4.SG":
#             return "Aerospace & Defense" if industry else "Industrials"
#         if ticker == "SYY.SG":
#             return "Food Distribution" if industry else "Consumer Defensive"
#         if ticker == 'NTXFY':
#             return 'Financial Services' if industry else 'Banks - Regional'
#         if ticker == 'PRSP':
#             return 'IT Services' if industry else 'Information Technology'
#         if ticker == 'PS':
#             return 'Software' if industry else 'Information Technology'


# # quite surprising to see international markets 
#         url = "https://finance.yahoo.com/quote/TICKER/profile?p=TICKER".replace("TICKER", str(ticker))
#         agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'

#         headers = {'User-Agent': agent}

#         response = requests.get(url, headers=headers)
        
#         if "Fund Family</span>" in response.text:
#             return "Fund"
        
#         i = 0         
#         while response.text.find(key, i) > 0: 
#             i = response.text.find(key, i) + 1
#             if i == -1: 
#                 break 
            
#             key_line = response.text[response.text.find(key):response.text.find(key)+300]
#             if "reactid" in key_line:
#                 if ">" not in key_line:
#                     continue
#                 key_line = key_line.split(">")
#                 return key_line[4].split("<")[0].replace("&amp;", "&")
            
#             elif "Fw(600)" in key_line:
#                 key_line = key_line[key_line.find('Fw(600)') : ].split(">")
#                 return key_line[1].split("<")[0].replace("&amp;", "&")                
                        
#         if key == "Sector(s)":
#             key = '<a href="https://finance.yahoo.com/sector/'

#             if response.text.find(key) > 0:
#                 key_line = response.text[response.text.find(key):response.text.find(key)+300]
#                 key_line = key_line.split(">")   
#                 result = key_line[1].replace("</a", "")                
#                 key_line = key_line[0]
#                 key_line = key_line[ key_line.find("data-symbol=") : ]                
#                 key_line = key_line[: key_line.find(" ")]
#                 key_line = key_line[key_line.find('"') : ].replace('"', "")
                
#                 key_line = list(key_line)
#                 for letter in ticker:
#                     if letter in key_line:
#                         key_line.remove(letter)
#                     else:
#                         return None 
#                 return result

#         return None 
    
#     except Exception:
#         # print(ticker)
#         return None 
#         # raise Unknown
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_industry(ticker):
#     try:
        
#         with RESTClient(constants.api_key) as client:
#             resp = client.reference_ticker_details(ticker)
#             return resp.industry if resp.industry != "" else get_yfinance(ticker, industry=True)

#     except HTTPError as e:
#         if "404" in str(e):
#             res = get_yfinance(ticker, industry=True)
#             if res:
#                 return res
#             return None 
#             # raise Unknown

#         if "429" in str(e):
#             time.sleep(60)
#             return get_industry(ticker)
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # TODO
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_sector(ticker):
#     try:
        
#         with RESTClient(constants.api_key) as client:
#             resp = client.reference_ticker_details(ticker)
#             return resp.sector if resp.sector != "" else get_yfinance(ticker, industry=False)
        
#     except HTTPError as e:
#         if "404" in str(e):
#             res = get_yfinance(ticker, industry=False)
#             if res:
#                 return res
#             # raise Unknown
#             return None 

#         if "429" in str(e):
#             time.sleep(60)
#             return get_sector(ticker)
# # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clean_up_res(res):
    try: 
        return res[res.find("=")+1:].replace("[", "").replace("]", "").replace("}", "").replace('"', "").replace("{{ubl", "").replace("{{plainlist", "").replace("*", "").replace("{{nowrap|", "").strip()
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def parse(d, word, count, s, break_point):
    try: 
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
            raise Exception("Pattern mismatch.")

        else:
            if 'Representatives' in word: 
                word = 'state'
            d[word.strip()] = clean_up_res(res)

        return d
    except Exception: 
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def go_shopping(l, s):
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

    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def page(probable_result_title):
    try: 
        htmled_tltle = probable_result_title.replace(" ", "%20")

        resp = requests.get(constants.WIKIPEDIA_SEARCH_URL.format(person=htmled_tltle)).json()

        page_one = next(iter(resp['query']['pages'].values()))
        revisions = page_one.get('revisions', [])

        s = list(revisions[0].values())[2]
        return s
    
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_wiki_page(name):
    try: 
        results = wikipedia.search(name)
        at = 0
        
        s = page(results[at]) 
        if "may refer to" in s: 
            at += 1
            s = page(results[at])  

        while "United States Senator" not in s and "United States representative" not in s and "U.S. representative" not in s and  "United States senator" not in s and "U.S. Representative" not in s and "U.S. House of Representatives" not in s and "United States House of Representatives" not in s:
            at += 1
            s = page(results[at])  
        
        return s 
    
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# https://stackoverflow.com/questions/7638402/how-can-i-get-the-infobox-from-a-wikipedia-article-by-the-mediawiki-api
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def wiki_search(name):

    try:
        official_name = name 
        
        if name in constants.CANONICAL_NAME_TO_WIKIPEIDA_PROBLEMATIC_CONVERSATIONS:
            name = constants.CANONICAL_NAME_TO_WIKIPEIDA_PROBLEMATIC_CONVERSATIONS[name]

        s = get_wiki_page(name)
        
        d = go_shopping(["birth_place ", "alma_mater ", "birth_date ", "education "], s)
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
    
        return Official(official_name, state, birth_date, birth_place, party, education, senate, house)
        
    except Exception:
        print(name)
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def congress_gov_get(name, d={}, party_only=False):
    try: 
        # Remove middle initial
        if name[len(name)-1] == ".":
            name = name[:len(name)-3].strip()
        
        if name in constants.CANONICAL_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS: 
            name = constants.CANONICAL_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]

        htmled_name = name.replace(" ", "%20").replace(",", "%2C")
        html = constants.CONGRESS_GOV_URL.format(name=htmled_name)
            
        result = requests.get(html).text
        
        result = result[result.find('<div><span class="visualIndicator">MEMBER</span></div>') : result.find('<li class="compact" style="display:none">    1.')]
            
        state = result[result.find('<strong>State:</strong>') : ] 
        state = state[ : state.find('</span>')]
        state = state[state.find('<span>') : ].replace("<span>", "")
        
        senate = house = None 

        if state: 
            party = result[result.find('<strong>Party:</strong>') : ] 
            party = party[ : party.find('</span>')]
            party = party[party.find('<span>') : ].replace("<span>", "")

            if party_only:
                return party 

            served = result[result.find('<strong >Served:</strong>') : ] 
            served = served[ : served.find('</span>')]
            served = served[served.find('<span>') : ].replace("<span>", "").replace('<ul class="member-served">\n', "").replace("<li>", "")
            
            if served.find("Senate: ")  > 0: 
                served_temp = served[served.find("Senate: ") + 8 : ] 
                senate = served_temp [ : served_temp.find("</li>")]
                d['senate'] = senate 
                
            if served.find("House: ")  > 0: 
                served_temp = served[served.find("House: ") + 7 : ] 
                house = served_temp [ : served_temp.find("</li>")]
                d['house'] = house 
                
        else:
            query = "{} site:www.congress.gov".format(name)

            result = requests.get(search(query)[0]).text

            party = result[result.find('<th scope="row" class="member_party">Party</th>') : ] 
            party = party[ party.find('<td>') + 4: party.find('</td>')]
        
            if party_only:
                return party 
                            
            query = ["Senate", "House"]
            
            for q in query: 
                if result.find('<th class="member_chamber">'+q+'</th>') > 0:
                    house = result[result.find('<th class="member_chamber">'+q+'</th>') : ] 
                    res = ""
                    while house.find("</td>") > 0: 
                        house_temp = house[ : house.find("</td>") ]
                        house = house[ house.find("</td>") + 4: ]
                        
                        house_temp = house_temp[house_temp.find("<td>") : ]
                        if not state: 
                            state = house_temp[ : house_temp.find(",")].replace("<td>", "")
                        house_temp = house_temp[house_temp.find("(") : ].replace("(", "").replace(")", "").strip()
                        res += house_temp + ", "

                    res = res.strip()
                    res = res[ : len(res) - 3]
                    
                    if not res: 
                        res = None 
                    d[q.lower()] = res


        d['state'] = state
        d['party'] = party

        return d 
    
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def parse(temp_result):
    try: 
        members = []
        column = 0 
        
        while temp_result.find(constants.DD_HTML) > -1: 
            jump = temp_result.find(constants.DD_HTML)
            
            if temp_result.find("</td>") < jump:
                column += 1 
                if column == 2:
                    temp_result = temp_result[temp_result.find(constants.DD_HTML) : ]
                    break 
            
            temp_result = temp_result[ jump + 4 : ]
            
            find = "</dd>"
            if find in temp_result:
                temp_result_local = temp_result [ : temp_result.find("</dd>") ]
                
            
            find = "<a"
            if find in temp_result_local:
                temp_result_local = temp_result_local[ temp_result_local.find("<a") : ]

            find = 'href="'
            link = None 
            if find in temp_result_local:
                link = temp_result_local[ temp_result_local.find(find) + len(find) : ] 
                link = link[ : link.find('"')]                

            find = '>' 
            if find in temp_result_local:
                temp_result_local = temp_result_local[ temp_result_local.find('>') + 1: ]
                

            temp_result_local = temp_result_local.replace("</a>", "").replace("Resident Commissioner", "")
            
            temp_result_local = temp_result_local.split(",")

            for i in itertools.islice(temp_result_local, 1, len(temp_result_local)-1):
                if 'title' in i:
                    temp_result += " " +  constants.DD_HTML + " " + i  + "</dd>"

            temp_result_local = temp_result_local[0]

            find = "<sup"
            if find in temp_result_local:
                temp_result_local = temp_result_local[ :temp_result_local.find(find) ]


            find = "<a"
            if find in temp_result_local: 
                temp_result_local = temp_result_local[temp_result_local.find(find)+len(find) : ]
            
            
            find = '<a href="/wiki/New_Progressive_Party_of_Puerto_Rico" class="mw-redirect" title="New Progressive Party of Puerto Rico">'
            if find in temp_result_local:
                temp_result_local = temp_result_local.replace(find, "")

            find = 'href="'
            if find in temp_result_local:
                link = temp_result_local[ temp_result_local.find(find) + len(find) : ] 
                link = link[ : link.find('"')]            
            
            temp_result_local = temp_result_local.replace("(", "").replace(")", "")
                
            find = ">"
            if find in temp_result_local:
                if 'from' not in temp_result_local[ temp_result_local.find(find) + len(find) : ]:
                    temp_result_local = temp_result_local[ temp_result_local.find(find) + len(find) : ]
                    

                
            finds = ["<span", "from", "until", "<a href"]
            for find in finds: 
                if find in temp_result_local:
                    temp_result_local = temp_result_local[ : temp_result_local.find(find) ] 
                    
            
            find = '>' 
            if find in temp_result_local:
                temp_result_local = temp_result_local[ temp_result_local.find(find) + len(find) : ]
            
                                    
            temp_result_local = temp_result_local.replace("/", "")

            if len(temp_result_local) > 0: 

                p = temp_result_local[len(temp_result_local.strip()) - 1 ].strip()
                if temp_result_local[len(temp_result_local.strip()) - 2 ] != " ":
                    p = temp_result_local.strip().split(" ")
                    p = p[len(p)-1]
                
                name = temp_result_local[ : len(temp_result_local.strip()) - len(p)].strip() 
                if len(name) > 0:
                    assert link
                    members.append((name, link))
                
                
        return temp_result, members 
    
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Given the year, this method returns a Congress object.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_congress(year):
    
    try: 
        # https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

        url = constants.WIKIPEDIA_CONGRESS_URL.replace("NUMBER", ordinal(year))

        result = requests.get(url).text

        og = '<td style="width: 50%;text-align: left; vertical-align: top;"><h4><span class='
        jump = result.find(og) 
        if jump == -1: 
            og = '<td style="text-align: left; vertical-align: top;">'
            jump = result.find(og) 

        temp_result = result[jump + len(og) : ]    
        temp_result, senate_members = parse(temp_result)
        _, house_members = parse(temp_result) 
        
        return Congress(year, senate_members, house_members)
    
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_redirection_link(link):
    res = requests.get("https://wikipedia.com/?".replace("?", link)).text
    
    find = '<link rel="canonical" href="https://en.wikipedia.org/wiki'
    res = res[ res.find(find) + len(find) : ] 
    # a possible redirection link 
    res = res [ : res.find('"')]
    
    return res.strip()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
