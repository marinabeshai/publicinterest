# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import helpers.search as search 
import utils.dict_utils as dict_utils  
import helpers.official as official
import utils.constants as constants 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Congress:
   # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    def __init__(self, number, senate_members, house_members):
        self.number = number 
        self._senate_members = senate_members
        self._house_members = house_members
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # def debug(self):
    #     return(
    #         "self.number :{}\n num_of_senators: {}\n senate_party: {}\nsenate_members: {}\nnum_of_representatives: {}\nhouse_party: {}\nhouse_members: {}".
    #         format(self.number, self.get_count_senate(), self.senate_party, self.senate_members, self.get_count_house(), self.house_party, self.house_members)
    #     )
   # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_everyone(self):
        l = []
        
        for name, link in self._house_members:
            name = name if name not in constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS else constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]
            l.append((name, link.strip()))
            
        for name, link in self._senate_members:
            name = name if name not in constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS else constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]
            l.append((name, link.strip()))
        
        return l
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_house_party(self):
        try: 
            d = {}

            for name, _ in self._house_members:
                name = name if name not in constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS else constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]
                p = search.congress_gov_get(name, party_only=True)
                d = dict_utils.increment_dictionary(d, p)
                
            return d 
        except:
            print(name, d, p)
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_senate_party(self):
        d = {}
        
        for name, _ in self._senate_members:
            name = name if name not in constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS else constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]
            p = search.congress_gov_get(name, party_only=True)
            d = dict_utils.increment_dictionary(d, p)
            
        return d 
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# THERE COULD BE DUPLICATES IN _SENATE _HOUSE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_officials(everyone=False, senate=False, house=False):
    try: 
        l = list(range(112, 118))
        
        all_officials_list = []
        all_officials_dict = {}

        for i in l:
            if everyone: 
                all_officials_list.append(search.get_congress(i).get_everyone())
            if senate: 
                all_officials_list.append(search.get_congress(i)._senate_members)
            if house: 
                all_officials_list.append(search.get_congress(i)._house_members)

        all_officials_list = [item for sublist in all_officials_list for item in sublist ]
        
        for name, link in all_officials_list:
            name = official.get_canonical_name(name) if name not in constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS else constants.NAMES_TO_CONGRESS_GOV_PROBLEMATIC_CONVERSIONS[name]
            
            possible_redirection_link = search.get_redirection_link(link)
            
            if possible_redirection_link not in all_officials_dict:
                all_officials_dict[possible_redirection_link] = name 
                    
        return all_officials_dict
    
    except: 
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_officials():
    return get_officials(everyone=True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_house_officials():
    return get_officials(house=True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_senate_officials():
    return get_officials(senate=True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_officials_state(everyone=[], house=[], senate=[]):
    try:
        l = []
        l.append(everyone)
        l.append(house)
        l.append(senate)      
        l = [x for sublist in l for x in sublist]
        
        
        d = {}
        for name in l:
            p = search.congress_gov_get(name, state_only=True)
            d = dict_utils.increment_dictionary(d, p)
            
        return d 
        
    except:
        print(name)
        raise constants.Unknown
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

