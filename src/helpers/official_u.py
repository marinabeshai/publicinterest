# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from utils.constants import DATE_FORMAT, Unknown
import gender_guesser.detector as gender
from datetime import date, datetime
import re
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Class for Official (either senator or representative).
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Official:
    def __init__(self, name, state, birth_date, birth_place, party, education, senate, house):
        self.name = name
        self.state = state
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.party = party
        self.education = education
        self.senate = senate
        self.house = house
        
    def check(self):
        return {"self.get_paperworkname()" : self.get_name(),
                "self.get_congress()" : self.get_congress(), 
                "self.get_birthdate()" : self.get_birthdate(), 
                "self.get_state()" : self.get_state(),
                "self.get_birth_place()" : self.get_birth_place(), 
                "self.get_party()" : self.get_party(), 
                "self.get_education()" : self.get_education(), 
                "self.get_num_of_years()" : self.get_seniority(),
                "self.get_num_of_degrees()": self.get_num_of_degrees()}
    
    def get_gender(self):
        d = gender.Detector()
        x =  d.get_gender(self.name.split(" ")[0])
        if "mostly" in x:
            return x.split("_")[1]
        return x 
        
    def get_name(self):
        assert self.name
        return self.name
   
    def get_state(self):
        assert self.state
        return self.state

    def get_birthdate(self):
        assert self.birth_date
        return datetime.strptime(self.birth_date, '%Y/%m/%d').strftime(DATE_FORMAT)

    def get_birth_place(self):
        assert self.birth_place
        return self.birth_place.split("|")[0].split("<")[0]
    
    def get_party(self):
        assert self.party 
        return self.party

    # Gives you a rough list of degrees per official. 
    def get_education(self):
        # assert self.education

        nl = []
        if not self.education:
            return nl 

        l = self.education.replace("\n", " ").replace("|", " ").replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ").split(" ")
        
        s = ""
        for word in l:
            s += word     
            s += " "
       
            if ")" in word:
                nl.append(s.strip())
                s = ""

        return nl 


    def get_congress(self):
            assert self.senate or self.house

            l = [self.senate, self.house]
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
        
    def get_num_of_degrees(self):
        try:
            ed = str(self.get_education()).replace("'","").replace("[", "").replace("]", "").split(" ")
            key = ["AA", "J.D.", "B.A.", "BS", "BA", "JD", "AB", "MAR", "MD", "MS", "OD", "PhD", "AAS", "MSS", "BCL", "MPP", "BBA", "LLM", "MBA", "MA", "LLB","MEd", "AS", "EdD", "MPA", "MSc", "MPH", "SM", "MPhil", "MAcc", "MIA", "ALB", "BDiv", "DVM", "BEng"]
            count = 0
            
            for word in ed:
                if word[len(word) - 1] == ")" or word[len(word) - 1] == ",":
                    word = word[ : len(word) - 1]
                    ed.append(word)
                    continue
                if len(word) > 5: 
                    continue
                if word in key:
                    count += 1 
                    
            return count 
        except:
            return None

    def get_seniority(self):
        assert self.senate or self.house
        
        l = [self.senate, self.house]
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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# https://www.geeksforgeeks.org/validating-roman-numerals-using-regular-expression/
# Returns true is num is a roman numeral. 
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
        raise(Unknown) 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
