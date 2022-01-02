# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from utils.constants import DATE_FORMAT, Unknown, DEGREES
import gender_guesser.detector as gender
from datetime import date, datetime
import re
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Class for Official (either senator or representative).
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Official:
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Constructor. 
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, name, state, birth_date, birth_place, party, education, senate, house):
        self.name = name
        self.state = state
        self._birth_date = birth_date
        self._birth_place = birth_place
        self.party = party
        self._education = education
        self._senate = senate
        self._house = house
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Returns probablistic gender of Official. 
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    "sam, jack "
    def get_gender(self):
        try: 
            d = gender.Detector()
            first_name = self.name.split(", ")[1].split(" ")[0]
            x =  d.get_gender(first_name)
            if "mostly" in x:
                return x.split("_")[1]
            return x 
        except Exception:
            print(self.name)
            raise Unknown
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
                
                if y == 'Present': y = date.today().year

                begin_congress = 93 + ((int(x) - 1973) // 2)
                end_congress = 93 + ((int(y) - 1973) // 2)
                res.append(list(range(begin_congress, end_congress+1)))

            return list(set(item for sublist in res for item in sublist))
        
        except Exception:
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
        problematic = {
            'Ron L Wyden' :'Ronald L Wyden',
            'Ron Wyden':'Ronald L Wyden',            
            'Angus S King': 'Angus S King, Jr.',            
            'Roy Blunt' : 'Roy D Blunt',            
            'Hon. Charles J. "Chuck" Fleischmann' : 'Hon. Charles J. Fleischmann',
            'Hon. Neal Patrick Dunn MD, FACS' :  'Hon. Charles J. Fleischmann' ,
            'Hon. Neal Patrick MD, Facs Dunn' :  'Hon. Charles J. Fleischmann' , 
            'Hon. Neal Patrick MD, FACS Dunn' : 'Hon. Charles J. Fleischmann',
            'Hon. James E Hon Banks' : 'Hon. James E. Banks'    ,
            'Maria Cantwell' : 'Maria E Cantwell',
            'Hon. Wm. Lacy Clay' : 'Hon. William Lacy Clay Jr.',
            'Tammy Duckworth' : 'Ladda Tammy Duckworth',
            'Angus S King' : 'Angus S King, Jr.',
            'Tom S Udall' : 'Thomas S Udall',
            'Thomas Udall': 'Thomas S Udall',
            'Hon. Greg Steube'  : 'Hon. William Greg Steube' ,
            'Hon. W. Greg Steube'  : 'Hon. William Greg Steube' ,
            'Hon. Michael Garcia' : 'Hon. Mike Garcia',           
            'Hon. Cindy Axne' : 'Hon. Cynthia Axne'}
            
        if name in problematic:
            name = problematic[name]
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
