# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from zmq import REP
from utils.constants import DATE_FORMAT, FEMALE_NAMES, MALE_NAMES, Unknown, DEGREES, MULTIPLE_INPUTS_PROBLEMATIC_CONVERSIONS, REPRESENTATIVE, SENATOR
import gender_guesser.detector as gender
from datetime import date, datetime
from utils.ptr_utils import isvalid
import re

from utils.ptr_utils import get_year
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Class for Official (either senator or representative).
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Official:
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Constructor. 
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, name, state, birth_date, birth_place, party, education, senate, house, asgts):
        self.name = name
        self.state = state
        self._birth_date = birth_date
        self._birth_place = birth_place
        self.party = party
        self._education = education
        self._senate = senate
        self._house = house
        self.asgts = asgts 
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check(self):
        return {"self.get_paperworkname()" : self.name,
                "self.get_congress()" : self.get_congress(), 
                "self.get_years_served()" : self.get_years_served(), 
                # "self.get_birthdate()" : self.get_birthdate(), 
                # "self.get_state()" : self.state,
                # "self.get_birth_place()" : self.get_birthplace(), 
                # "self.get_party()" : self.party, 
                # "self.get_education()" : self.get_education(), 
                # "self.get_num_of_years()" : self.get_seniority(),
                # "self.get_num_of_degrees()": self.get_num_of_degrees(),
                # "self.has_jd": self.has_JD(), 
                # "self.asgts" :  self.asgts
                }
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_age(self):
        birthdate = datetime.strptime(self.get_birthdate(), DATE_FORMAT).date()
        x = date.today()
        return (x - birthdate).days // 365
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns birthdate of Official in DATE_FORMAT.
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_birthdate(self):
        assert self._birth_date
        return datetime.strptime(self._birth_date, '%Y/%m/%d').strftime(DATE_FORMAT)
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns birthplace of Official.
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_birthplace(self):
        assert self._birth_place
        return self._birth_place.split("|")[0].split("<")[0]
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns a rough list of degrees per official. 
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_education(self):
        try: 
            nl = []
            if not self._education:
                return nl 

            l = self._education.replace("ist", "").replace("{{unbulleted list", "").replace("\n", " ").replace("|", " ").replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ").split(" ")
            
            s = ""
            for word in l:
                s += word     
                s += " "
        
                if ")" in word:
                    nl.append(s.strip())
                    s = ""

            return nl 
        except Exception:
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_years_served(self):
        try: 
            l = [self._senate, self._house]
            ranges = []
            
            for phrase in l:
                if not phrase: 
                    continue
                if "," in phrase:
                    lprime = phrase.split(",")
                    for i in lprime: ranges.append(i) 
                else:
                    ranges.append(phrase) 

            res = []
            for r in ranges:
                l = r.split("-")
                x = l[0]
                y = l[1]
                
                if y == 'Present': y = date.today().year
                
                res.append(list(range(int(x), int(y) + 1)))
            
            return sorted(list(set(item for sublist in res for item in sublist)))
                                       
        except Exception:
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns list of Congresses that Official participated in as a repesentative or senator.
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_congress(self):
        try: 
            assert self._senate or self._house

            l = [self._senate, self._house]
            ranges = []
            res = []
            
            for phrase in l:
                if not phrase: 
                    continue
                if "," in phrase:
                    lprime = phrase.split(",")
                    for i in lprime: ranges.append(i) 
                else:
                    ranges.append(phrase) 
                    
            for r in ranges: 
                l = r.split("-")
                x = l[0]
                y = l[1]
                
                if y == 'Present': y = date.today().year + 1 

                begin_congress = 93 + ((int(x) - 1973) // 2)
                end_congress = 93 + ((int(y) - 1973) // 2)
                
                # Biggest corner case known to man. 
                if self.name == 'Loeffler, Kelly' or self.name == 'Cochran, Thad':
                    end_congress += 1 
                    
                res.append(list(range(begin_congress, end_congress)))

            return sorted(list(set(item for sublist in res for item in sublist)))
        
        except Exception:
            print(self.name)
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns list of degree abbreviations that Official completed.
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_degrees(self):
        try: 
            res = []
            ed = self.get_education()
            if len(ed) == 0: return res
            ed = str(ed).replace("'","").replace("[", "").replace("]", "").replace("''", "").split(" ")

                        
            for word in ed:                
                if not word: 
                    continue                
                if word[len(word) - 1] == ")" or word[len(word) - 1] == "," or word[len(word) - 1] ==  '"':
                    word = word[ : len(word) - 1]
                    ed.append(word)
                    continue
                if len(word) > 5: 
                    continue
                if word in DEGREES:
                    res.append(word)
                    
            return res    
        except Exception:
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns number of degrees that Official completed.
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_num_of_degrees(self):
        try: 
            return len(self.get_degrees())
        except:
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns number of years in Office in total (including Senate and House, if applicable).
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_seniority(self):
        try: 
            assert self._senate or self._house
            
            l = [self._senate, self._house]
            years = 0 
            
            for range in l:
                if not range: 
                    continue
                if "," in range:
                    lprime = range.split(",")
                    for i in lprime: l.append(i) 
                    
                    continue
                x, y = range.split("-")
                if y == "Present":
                    y = date.today().year
                    
                years += int(y) - int(x)    
                
            return years if years > 0 else 1 
        except Exception:
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns True iff Official has any law degree (defined as a JD, LLM, LLB, or BCL). 
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def has_JD(self):
        try: 
            z = self.get_degrees()
            if not z:
                return False 

            return "J.D." in z or "JD" in z or "LLM" in z or "LLB" in z  or "BCL" in z
        except Exception:
            raise Unknown
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# From https://www.geeksforgeeks.org/validating-roman-numerals-using-regular-expression/
# Returns true if num is a roman numeral. 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def is_roman_number(num):
    try: 
        num = num.upper()
        
        pattern = re.compile(r"""   
                                    ^M{0,3}
                                    (CM|CD|D?C{0,3})?
                                    (XC|XL|L?X{0,3})?
                                    (IX|IV|V?I{0,3})?$
                """, re.VERBOSE)

        return re.match(pattern, num)

    except Exception:
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Returns a "truthful" name of the format: LAST_NAME, FIRST_NAME [OPTIONAL_MIDDLE_INITIAL.]
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_canonical_name(name):
    try:
            
        if name in MULTIPLE_INPUTS_PROBLEMATIC_CONVERSIONS:
            name = MULTIPLE_INPUTS_PROBLEMATIC_CONVERSIONS[name]
        name = name.replace('Hon. ', '').replace('Mr. ', '').replace('Honorable', '').replace('Mrs. ', '').replace('None ', '').replace('Hon ', '').replace('Dr ', '')
        
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
            nl[1] = nl[1][0] + "."            
            return (nl[len(nl) - 1] + ", " + nl[0] + " " + nl[1])
        
        return (nl[len(nl) - 1] + ", " + nl[0])     
    
    except Exception: 
        raise Unknown 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Returns probablistic gender of Official. 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_gender(name, link=""):
    try: 

        if name == 'Butterfield, G. K.' or name == 'Krishnamoorthi, S. R.' or name == 'McConnell Jr., A. M.' or name == 'Conaway, K. M.':
            return 'male'
        
        if name == 'Emerson, Jo A.':
            return 'female'

        if ", " in name:
            name = name.split(", ")[1]
        
        name = name.split(" ")[0]
        if name in FEMALE_NAMES:
            return 'female'
        if  name in MALE_NAMES:
            return 'male'
        
        d = gender.Detector()
        x =  d.get_gender(name)
        if "mostly" in x:
            return x.split("_")[1]
        
        if "unknown" in x and link:
            link = link[ 1: ]
            return get_gender(link.split("_")[0])
        
        return x 
    except Exception:
        print(name)
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_name(t):
    try:
        if REPRESENTATIVE in t and isvalid(t[REPRESENTATIVE]): 
            return get_canonical_name(t[REPRESENTATIVE])
        
        if SENATOR in t and isvalid(t[SENATOR]): 
            return get_canonical_name(t[SENATOR])

    except Exception:
        print(t)
        raise Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------