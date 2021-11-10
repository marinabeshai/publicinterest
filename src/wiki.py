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
    
    # def debug(self):
    #     print("name ",  self.name)
    #     print("jr ",  self.jr)
    #     print("state " , self.state)
    #     print("term_start " , self.term_start)
    #     print("birthplace " , self.birth_place)
    #     print("party " , self.party)
    #     print("education " , self.education)
    #     print(" get_num_of_years " , self.get_num_of_years() )
        
    def get_congress(self):
        return 93 + (datetime.strptime(self.term_start, '%B %d, %Y').date().year - 1973) / 2 
        
        

        # 3000 - term_start
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
