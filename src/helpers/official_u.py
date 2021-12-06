# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from datetime import date, datetime
import re
from utils.constants import DATE_FORMAT
import gender_guesser.detector as gender
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 
# 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def not_null(val):
    assert val is not None 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions per person.
# trans_per_person_total={'Max': 5, 'Sam': 20, ...}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Official:
    def __init__(self, paperwork_name,  jr, state, term_start, term_end, birth_date, birth_place, party, alma_mater, education):
        self.paperwork_name = paperwork_name
        self.jr = jr
        self.state = state
        self.term_start = term_start
        self.term_end = term_end
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.party = party
        if alma_mater:
            self.education = alma_mater
        else:
            self.education = education
        
    def check(self):
        return {"self.get_paperworkname()" : self.get_paperworkname(),
                "self.get_congress()" : self.get_congress(), 
                "self.get_birthdate()" : self.get_birthdate(), 
                "self.get_canonical_name()": self.get_canonical_name(),
                "self.get_jr()" : self.get_jr(), 
                "self.get_state()" : self.get_state(),
                "self.get_term_start()" : self.get_term_start(),
                "self.get_birth_place()" : self.get_birth_place(), 
                "self.get_party()" : self.get_party(), 
                "self.get_education()" : self.get_education(), 
                "self.get_num_of_years()" : self.get_num_of_years(),
                "self.get_num_of_degrees()": self.get_num_of_degrees()}
    
    def get_gender(self):
        d = gender.Detector()
        x =  d.get_gender(self.paperwork_name.split(" ")[0])
        if "mostly" in x:
            return x.split("_")[1]
        return x 
        
            
        
    def get_paperworkname(self):
        not_null(self.paperwork_name)
        return self.paperwork_name
        
    def get_congress(self):
        not_null(self.term_start)

        begin_congress = 93 + ((datetime.strptime(self.term_start, '%B %d, %Y').date().year - 1973) // 2)
        if self.term_end:
            end_congress = 93 + ((datetime.strptime(self.term_end, '%B %d, %Y').date().year - 1973) // 2)
        else:
            end_congress = 93 + ((date.today().year - 1973) // 2)

        return list(range(begin_congress, end_congress+1)) 


        # 3000 - term_start
    def get_birthdate(self):
        not_null(self.birth_date)
        return datetime.strptime(self.birth_date, '%Y/%m/%d').strftime(DATE_FORMAT)

    def get_canonical_name(self):
        not_null(self.paperwork_name)
        return get_canonical_name(self.paperwork_name)

    def get_jr(self):
        not_null(self.jr)
        return self.jr

    def get_state(self):
        not_null(self.state)
        return self.state

    def get_term_start(self):
        not_null(self.term_start)
        return datetime.strptime(self.term_start, '%B %d, %Y').strftime(DATE_FORMAT)

    def get_birth_place(self):
        not_null(self.birth_place)
        return self.birth_place

    def get_party(self):
        not_null(self.party)
        return self.party

    # Gives you a rough list of degrees per official. 
    def get_education(self):
        not_null(self.education)

        l = self.education.replace("\n", " ").replace("|", " ").replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ").split(" ")
        
        s = ""
        nl = []
        for word in l:
            s += word     
            s += " "
       
            if ")" in word:
                nl.append(s.strip())
                s = ""

        assert nl != []
        return nl 
        
    def get_num_of_degrees(self):
        not_null(self.education)
        ed = str(self.get_education())
        key = ["BS", "BA", "JD", "AB", "MAR", "MD", "MS", "OD", "PhD", "AAS", "MSS", "BCL", "MPP", "BBA", "LLM", "MBA", "MA", "LLB","MEd"]
        count = 0
        
        

        for k in key:
            where_to_start = 0
            while ed.find(k, where_to_start) > 0:
                x = ed.find(k, where_to_start)
                if ed[ x - 1: x+len(k)] not in key and ed[x: x+len(k)] == k and ed[ x: x+len(k)+1] not in key:
                    count += 1 
                where_to_start = x + 1 
                
                
        return count 

    def get_num_of_years(self):
        today = date.today()
        term_start = datetime.strptime(self.term_start, '%B %d, %Y').date()
        diff = today.year - term_start.year
        return diff if diff != 0 else 1
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def is_roman_number(num):
    num = num.upper()
    
    pattern = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE)

    if re.match(pattern, num):
        return True

    return False
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def corner_cases(res):
    if res == "King, Angus":
        return "King Jr., Angus"
    
    if res == "Udall, Tom":
        return "Udall, Thomas"
    
    if res == "Wyden, Ron" or res == "Wyden, Ron L" or res == "Wyden, Ronald L": 
        return "Wyden, Ronald L"
    
    return res 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_canonical_name(name):
        nl = (name.replace(",", "").split(" "))

        for x in nl:
            if not x:
                nl.remove(x)

        if nl[len(nl) - 2] == ",":
             nl.pop(len(nl) - 2)
             nl[len(nl) - 2] = nl[len(nl) - 2] + ","
        
        if is_roman_number( nl[len(nl) - 1]):            
            s = " "
            
            for index in range(len(nl[len(nl) - 1])):
                s += nl[len(nl) - 1][index].capitalize()
                

            nl[len(nl) - 2] = nl[len(nl) - 2]  + s
            nl.pop(len(nl) - 1)


        if nl[len(nl) - 1] == "Jr."  or nl[len(nl) - 1] == "Jr" or nl[len(nl) - 1] == "jr":
            nl[len(nl) - 2] = nl[len(nl) - 2]  + " Jr."
            nl.pop(len(nl) - 1)
                        
        if len(nl) > 2:
            return corner_cases(nl[len(nl) - 1] + ", " + nl[0] + " " + nl[1])
        
        return corner_cases(nl[len(nl) - 1] + ", " + nl[0])      
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
