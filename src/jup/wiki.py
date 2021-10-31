from numpy import diff, where
import wikipedia 
import requests
from datetime import date, datetime

def go_shopping(l, s, d):
    count = "0" 
    
    while l:
        
        w = l.pop()
        i = s.find(w)
        
        if i == -1 and "jr/sr" in w and int(count) < 9:
            count = str(int(count) + 1)
            l.append("jr/sr"+count) 
            pass 
        
        elif count == "10":
            return None 
        
        elif i == -1:
            pass
       
       
        else: 
            where_to_stop = len(w) + i 
            
            while s[where_to_stop] != "|":
                where_to_stop += 1             
            
            res = s[i+len(w): where_to_stop]
            
            d[w.strip()] = res[res.find("=")+1:].replace("[", "").replace("]", "").replace('"', "").strip()

    
    return d, count 
    # 


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions per person.
# trans_per_person_total={'Max': 5, 'Sam': 20, ...}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Official: 
    def __init__(self, name, jr, state, term_start, birth_date, birth_place, party, alma_mater, education):
        self.name = name
        self.jr = jr 
        self.state = state
        self.term_start = term_start
        self.birthdate = birth_date
        self.birth_place = birth_place
        self.party = party
        if alma_mater:
            self.education = alma_mater
        else:
            self.education = education
    
    def debug(self):
        print("name ",  self.name)
        print("jr ",  self.jr)
        print("state " , self.state)
        print("term_start " , self.term_start)
        print("birthplace " , self.birth_place)
        print("party " , self.party)
        print("education " , self.education)
        print(" get_num_of_years " , self.get_num_of_years() )
        
        
    def get_birthdate(self):
        return self.birthdate
    
    def get_name(self):
        return self.name
    
    def get_jr(self):
        return self.jr

    def get_state(self):
        return self.state

    def get_term_start(self):
        return self.term_start
    
    # def get_term_start_year(self):
    #     return int(self.term_start.split(",")[1].strip())

    def get_birth_place(self):
        return self.birth_place

    def get_party(self):
        return self.party

    def get_education(self):
        return self.education
    
    def get_num_of_years(self):
        # if not self.term_start:
        #     print(self.debug())
        today = date.today()
        term_start = datetime.strptime(self.term_start, '%B %d, %Y').date()    
        diff = today.year - term_start.year
        return diff if diff != 0 else 1 
        
        
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def page(probable_result_title):        
    htmled_tltle = probable_result_title.replace(" ", "%20")

    resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={person}&rvsection=0'.format(person=htmled_tltle)).json()
        
    page_one = next(iter(resp['query']['pages'].values()))
    revisions = page_one.get('revisions', [])



    s = list(revisions[0].values())[2]
    return s 

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# https://stackoverflow.com/questions/7638402/how-can-i-get-the-infobox-from-a-wikipedia-article-by-the-mediawiki-api
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def wiki_search(name):

    results = wikipedia.search(name)
    at = 0 
    s = ""
    while "politician" not in s:
        s = page(results[at])
        at += 1 

        
    l = ["name ", "jr/sr ", "birth_place ", "party ", "alma_mater ", "education ", "birth_date "]

    
    d, count = go_shopping(l, s, {})
    search_name = d.get("name", None)
    jr = d.get("jr/sr", None)
    birth_place = d.get("birth_place", None)
    party = d.get("party", None)
    alma_mater = d.get("alma_meter", None)
    education = d.get("education", None)
    birth_date = d.get("birth_date", None)

    if count == "0": 
        f1 = "state "
        f2 = "term_start "
    else: 
        f1 = "state"+count
        f2 = "term_start"+count
    
    
    l = [f1.strip(), f2.strip()]
    d, _ = go_shopping(l, s, d)

    state = d.get(f1.strip(), None)
    term_start = d.get(f2.strip(), None)

    x = Official(search_name, jr, state, term_start, birth_date, birth_place, party, alma_mater, education)
    

    return x
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# {{short description|Former United States Senator from New Mexico}}
# {{About|the senator from New Mexico|the senator from Colorado, his cousin|Mark Udall}}
# {{Use mdy dates|date=September 2015}}
# {{Infobox officeholder
# | name                = Tom Udall
# | image               = Tom Udall official photo.jpg
# | office = [[List of ambassadors of the United States to New Zealand|United States Ambassador to New Zealand]]
# | status = Designate
# | president = [[Joe Biden]]
# | term_start = TBD
# | term_end = 
# | succeeding = [[Scott Brown (politician)|Scott Brown]]
# | predecessor = [[Scott Brown (politician)|Scott Brown]]
# | successor = 
# | office1 = [[List of ambassadors of the United States to New Zealand|United States Ambassador to Samoa]]
# | status1 = Designate
# | president1 = Joe Biden
# | term_start1 = TBD
# | term_end1 = 
# | succeeding1 = Scott Brown
# | predecessor1 = Scott Brown
# | successor1 = 
# | jr/sr2               = United States Senator
# | state2               = [[New Mexico]]
# | term_start2          = January 3, 2009



# show more (open the raw output data in a text editor) ...

# | education           = [[Prescott College]] ([[Bachelor of Arts|BA]])<br>[[Downing College, Cambridge]] ([[Bachelor of Laws|LLB]])<br>[[University of New Mexico]] ([[Juris Doctor|JD]])
# | signature           = Tom Udall signature.png
# }}
# '''Thomas Stewart Udall''' ({{IPAc-en|ˈ|j|u|d|ɔː|l}} {{Respell|YOO|doll}}; born May 18, 1948) is an American diplomat, lawyer, and politician who served as a [[United States Senate|United States Senator]] for [[New Mexico]] from 2009 to 2021. A member of the [[Democratic Party (United States)|Democratic Party]], he served as the [[United States House of Representatives|U.S. Representative]] for {{ushr|New Mexico|3|}} from 1999 to 2009 and was the [[New Mexico Attorney General's Office|Attorney General of New Mexico]] from 1991 to 1999. A member of the [[Udall family]], he is the son of [[Stewart Udall]], the nephew of [[Mo Udall]], and the cousin of [[Mark Udall]]. He was the [[Dean of the House|dean]] of [[United States congressional delegations from New Mexico|New Mexico's congressional delegation]]. Udall was first elected in the [[2008 United States Senate election in New Mexico|2008 Senate race]]. He did not seek a third term in [[2020 United States Senate election in New Mexico|2020]], making him the only Democratic senator to retire that cycle. On July 16, 2021, President [[Joe Biden]] nominated Udall to serve as [[United States Ambassador to New Zealand]] and [[United States Ambassador to New Zealand|Samoa]].<ref name="WHBio"/>
# Thomas Udall


# {{redirect|Senator Perdue}}
# {{short description|American politician, businessman, and former U.S. senator from Georgia}}
# {{Use American English|date = September 2018}}
# {{Use mdy dates|date=December 2020}}
# {{Infobox officeholder
# | name                = David Perdue
# | image               = David Perdue, Official Portrait, 114th Congress.jpg
# | jr/sr               = United States Senator
# | state               = [[Georgia (U.S. state)|Georgia]]
# | term_start          = January 3, 2015
# | term_end            = January 3, 2021
# | predecessor         = [[Saxby Chambliss]]
# | successor           = [[Jon Ossoff]]
# | birth_name          = David Alfred Perdue Jr.
# | birth_date          = {{birth date and age|1949|12|10}}
# | birth_place         = [[Macon, Georgia]], U.S.
# | death_date          = 
# | death_place         = 
# | party               = [[Republican Party (United States)|Republican]]
# | spouse              = {{marriage|Bonnie Dunn|August 1972}}
# | children            = 3
# | relatives           = [[Sonny Perdue]] (cousin)
# | education           = [[Georgia Institute of Technology]] ([[Bachelor of Science|BS]], [[Master of Science|MS]])
# | net_worth           = [[US$]] 15.9 million (2021)<ref name="networth">{{cite web |url=https://www.rollcall.com/wealth-of-congress |title=Ranking the Net Worth of the 115th |work=rollcall.com|access-date=August 5, 2019}}</ref>
# | occupation          = {{hlist|Politician|businessman}}
