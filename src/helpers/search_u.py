# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from re import X
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
from random import randint

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
            
        if ticker in constants.CRYPTOCURRENCIES:
            return 'Cryptocurrency'
        if ticker in constants.FUNDS:
            return 'Fund'
        if ticker in constants.TRUSTS:
            return 'Trust'       
        
        changed = False
        if ticker in constants.SOME_WRONG_TICKERS:
            ticker = constants.SOME_WRONG_TICKERS[ticker]
            changed = True     
        
        if ticker in constants.MANUAL_FIXES:
            if industry: 
                return constants.MANUAL_FIXES[ticker]['industry']
            return constants.MANUAL_FIXES[ticker]['sector']
        
        if '.' in ticker and not changed: 
            ticker = ticker[:ticker.find('.')]        
        
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
    
    except Exception as e:
        print(e)
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
            return resp.industry if resp.industry else get_yfinance(ticker, industry=True)

    except HTTPError as e:
        if "404" in str(e):
            return get_yfinance(ticker, industry=True) 

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
            return resp.sector if resp.sector else get_yfinance(ticker, industry=False)
        
    except HTTPError as e:
        if "404" in str(e):
            return get_yfinance(ticker, industry=False) 

        if "429" in str(e):
            time.sleep(60)
            return get_sector(ticker)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
def page(probable_result_title, text=False):
    try: 
        htmled_tltle = probable_result_title.replace(" ", "%20")

        if text:
            return requests.get(constants.WIKIPEDIA_SEARCH_URL.format(person=htmled_tltle)).text
        
        resp = requests.get(constants.WIKIPEDIA_SEARCH_URL.format(person=htmled_tltle)).json()

        page_one = next(iter(resp['query']['pages'].values()))
        revisions = page_one.get('revisions', [])

        s = list(revisions[0].values())[2]
        return s
    
    except Exception:
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_wiki_page(name, text=False):
    try: 
        results = wikipedia.search(name)
        at = 0
        
        s = page(results[at], text) 
        
        if "may refer to" in s: 
            at += 1
            s = page(results[at], text)  

        while "United States Senator" not in s and "United States representative" not in s and "U.S. representative" not in s and  "United States senator" not in s and "U.S. Representative" not in s and "U.S. House of Representatives" not in s and "United States House of Representatives" not in s:
            at += 1
            s = page(results[at], text)  
        
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
        d = congress_gov_get(official_name, d)

        birth_place = d.get("birth_place", None)
        
        education = d.get("alma_mater", None)
        if not education:
            education = d.get("education", None)

        birth_date = d.get("birth_date", None)
        state = d.get("state", None)
        party = d.get("party", None)
        senate = d.get("senate", None)
        house = d.get("house", None)
        
        asgts = get_committee_assignments(official_name)
    
        return Official(official_name, state, birth_date, birth_place, party, education, senate, house, asgts)
        
    except Exception:
        print(name)
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def congress_gov_get(name, d={}, party_only=False, state_only=False, tries=0):
    try: 
        if tries == 2: 
            return d 

        if name == 'Cherfilus-McCormick, Sheila' and party_only:
            return 'Democratic'

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}

        # Remove middle initial
        if name[len(name)-1] == ".":
            name = name[:len(name)-3].strip()
        
        if name in constants.CANONICAL_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS: 
            name = constants.CANONICAL_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]

        htmled_name = name.replace(" ", "%20").replace(",", "%2C")
        html = constants.CONGRESS_GOV_URL.format(name=htmled_name)

        result = requests.get(html, headers).text
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
            if ',' in name:                
                name = name.split(" ")[0]
            else:                 
                name = name.split(" ")
                name = name[len(name)-1]
            return congress_gov_get(name, d=d, party_only=party_only, state_only=state_only, tries=tries+1)


        d['state'] = state
        d['party'] = party

        if state_only:
            return state 
        
        return d 
    
    except HTTPError as e: 
        if '429' in str(e):
            print(e)
            time.sleep(randint(30,40))
            
            return congress_gov_get(name, d, party_only=party_only)
        
        
    except Exception:
        print(name)
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

def get_link_from_text(res, find='<link rel="canonical" href="https://en.wikipedia.org/wiki'):
    res = res[ res.find(find) + len(find) : ] 
    # a possible redirection link 
    res = res [ : res.find('"')]
    return res.strip()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_redirection_link(link, get_wiki_link=False):    
    if get_wiki_link:
        res = requests.get(link).text
    else: 
        res = requests.get("https://wikipedia.com/?".replace("?", link)).text
    
    return get_link_from_text(res)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_wiki_link(name):    
    if name in constants.CANONICAL_NAME_TO_WIKIPEIDA_PROBLEMATIC_CONVERSATIONS:
        name = constants.CANONICAL_NAME_TO_WIKIPEIDA_PROBLEMATIC_CONVERSATIONS[name]

    res = get_wiki_page(name, text=True)
    curlid=  get_link_from_text(res, find='pageid"').replace(":", "").replace(",", "")
    html = "https://en.wikipedia.org/?curid=" + curlid

    return get_redirection_link(html, get_wiki_link=True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_committee_assignments(name):
    if name == 'Greene, Marjorie T.':
        return ['House Committee on Budget (2021-2022)', 'Committee on Education and the Workforce (2021-2022)']
    
    if name == 'Loeffler, Kelly':
        return ['Committee on Health Education Labor & Pensions (2020-2021)', 'Subcommittee on Children and Families (2020-2021)',
        'Subcommittee on Employment and Workplace Safety (2020-2021)', 'Primary Health and Retirement Security (2020-2021)', 'Joint Economic Committee (2020-2021)', 'Committee on Veterans Affairs (2020-2021)',
        'Committee on Agriculture, Nutrition, & Forestry (2020-2021)', 'Conservation, Forestry, and Natural Resources (2020-2021)', 'Livestock, Marketing, and Agriculture Security (2020-2021)']

    if name not in constants.CANONICAL_TO_BALLOTPEDIA_PROBLEMATIC_CONVERSIONS:
        name = name.replace(",", "").split(" ")
        name = name[1] + "_" + name[0]
    else:
        name = constants.CANONICAL_TO_BALLOTPEDIA_PROBLEMATIC_CONVERSIONS[name]

    headers = { 
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    link = f"https://ballotpedia.org/{name}"
    res = requests.get(link, headers).text
    
    find = 'id="Committee_assignments">Committee assignments</span>'
    res = res[res.find(find) + len(find) : ]
    
    finds = ['Key votes</a></span></h2>', 'id="Elections">Elections</span>', 'id="Elections">Elections</span></h2>', 'New York State Assembly</span></h3>', '"Key_votes">Key votes</span></h2>', '>Pennsylvania House</span></h3>', 'State Senate</span></h3>', 'session</span></h4>', 'legislation</span>', 'New York Assembly</span></h3>', 'North Carolina Senate</span></h3>', 'State House</span></h3>', 'State senate</span></h3>', 'Iowa House of Representatives</span></h3>', 'Maryland Senate</span></h3>', 'Issues</span></a>', 'Georgia Senate</span></a>']
    for find in finds: 
        if find in res: 
            res = res[ : res.find(find) + len(find) ]

    
    year = None 
    l = []
    
    H3 = '<h3>'
    H4 = '<h4>'
    LI = '<li>'
    
    LI_SPECIAL = '<li class="subcommittee">'
    while LI_SPECIAL in res or LI in res or H4 in res: 

        while res.find(H3) < res.find(H4) and res.find(H4) < res.find(LI) and res.find(H4) > 0 and res.find(H3) > 0:        
            res = res[ res.find(H3) + len(H3) : ]    
            type = res [ : res.find("</h3")] 
            if '>' in type:
                type = type[ type.find(">") + 1 : ]
            if '<' in type:
                type = type[ : type.find("<")  ]
            
            if type == 'U.S. House' or type == 'U.S. Senate':
                break 
            
        if  res.find(H3) < res.find(LI) and res.find(H3) > 0:
            res = res[ res.find(H3) + len(H3) : ]    
            year = res [ : res.find("</h3")] 
            if '>' in year:
                year = year[ year.find(">") + 1 : ]
            if '<' in year:
                year = year[ : year.find("<")  ]
            if len(year) == 7:
                year = year.split("-")
                year = year[0] + "-20" + year[1]
            continue
        

        if  res.find(H4) < res.find(LI) and res.find(H4) > 0:
            res = res[ res.find(H4) + len(H4) : ]    
            year = res [ : res.find("</h4")] 
            if '>' in year:
                year = year[ year.find(">") + 1 : ]
            if '<' in year:
                year = year[ : year.find("<")  ]
            if len(year) == 7:
                year = year.split("-")
                year = year[0] + "-20" + year[1]
            continue
        

        one = (res.find(LI_SPECIAL) < res.find(LI)) and (res.find(LI_SPECIAL) > 0)
        another = res.find(LI_SPECIAL) > 0 and res.find(LI) < 0
        if one or another: 
            res = res[ res.find(LI_SPECIAL) + len(LI_SPECIAL) : ]
            local_res = res [ : res.find("</li>")] 
            if ", <i>" in local_res:
                local_res = local_res.split(", <i>")[0]
            if ">" in local_res:
                local_res = local_res [ local_res.find(">") + 1 : ]
            if "</a" in local_res:
                local_res = local_res [ : local_res.find("</a")]

            ans = local_res.replace("&#39;", "'").replace("&amp;", "&").replace("<li>", "").replace("The Subcommittee", "Subcommittee").replace("(Chairman)", "").replace("(Chairwoman)", "").replace("United States", "").replace("House of Representatives", "House").replace(", Chairman", "").replace(", Chairwoman", "").replace("House of Representatives", "").replace("- Chair", "")
            if '</i>' not in ans:
                if ">" in ans:
                    ans = ans[ans.find(">") + 1 : ]
                l.append(ans.strip() + " (" + year + ")" )
            
        else: 

            h4 = res.find(H4)
            li = res.find(LI)
            lispecial = res.find(LI_SPECIAL)
            
            if h4 < li and h4 < lispecial and h4 > 0:
                res = res[ h4 + len(H4) : ]
            elif lispecial < li and lispecial > 0: 
                res = res[ lispecial : ]
            elif lispecial > 0 and li < 0:
                res  = res[ lispecial : ]
            elif li > 0: 
                res = res[ li + len(LI) : ]
            #     print(res)
            #     print('\n\n\n')
            else:
                break 

            local_res = res [ : res.find("</li>")] 
            if "<sup" in local_res:
                local_res = local_res [ : local_res.find("<sup")]
            if ", <i>" in local_res:
                local_res = local_res.split(", <i>")[0]
            if ">" in local_res:
                local_res = local_res [ local_res.find(">") + 1 : ]
            if "</a" in local_res:
                local_res = local_res [ : local_res.find("</a")]
            
            if year: 
                ans = local_res.replace("&#39;", "'").replace("&amp;", "&").replace("<li>", "").replace("The Subcommittee", "Subcommittee").replace("(Chairman)", "").replace("(Chairwoman)", "").replace("United States", "").replace("House of Representatives", "House").replace(", Chairman", "").replace(", Chairwoman", "").replace("House of Representatives", "").replace("- Chair", "")
                if '</i>' not in ans:
                    if ">" in ans:
                        ans = ans[ans.find(">") + 1 : ]
                    l.append(ans.strip() + " (" + year + ")" )
                    
    return l 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
