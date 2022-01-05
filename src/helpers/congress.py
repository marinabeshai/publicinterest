# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import helpers.search_u as search 
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
    def debug(self):
        return(
            "self.number :{}\n num_of_senators: {}\n senate_party: {}\nsenate_members: {}\nnum_of_representatives: {}\nhouse_party: {}\nhouse_members: {}".
            format(self.number, self.get_count_senate(), self.senate_party, self.senate_members, self.get_count_house(), self.house_party, self.house_members)
        )
   # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_count_total(self):    
        return (len(self._house_members) + len(self._senate_members))
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_count_senate(self): 
        return len(self._senate_members)
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_count_house(self):        
        return len(self._house_members) 
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_everyone(self):
        l = []
        
        for name, link in self._house_members:
            l.append((name, link.lower().strip()))
        for name, link in self._senate_members:
            l.append((name, link.lower().strip()))
        
        return l
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_house_party(self):
        d = {}
        l = []
        
        for name, _ in self._house_members:
            l.append(name)

        for name in l:
            d = dict_utils.increment_dictionary(d, search.congress_gov_get(name, party_only=True))
            
        return d 
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_senate_party(self):
        d = {}
        l = []
        
        for name, _ in self._senate_members:
            l.append(name)
            
        for name in l:
            d = dict_utils.increment_dictionary(d, search.congress_gov_get(name, party_only=True))
            
        return d 
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_officials():
    l = list(range(112, 118))
    all_officials_list = []
    all_officials_set = set()
    
    for i in l:
        all_officials_list.append(search.get_congress(i).get_everyone())
        
    all_officials_list = [item for sublist in all_officials_list for item in sublist ]
    
    c = 1
    for name, link in all_officials_list:
        print(c)
        c += 1
        possible_redirection_link = search.get_redirection_link(link)

        if (official.get_canonical_name(name), possible_redirection_link.lower()) not in all_officials_set:
            all_officials_set.add((official.get_canonical_name(name), possible_redirection_link.lower()))


    res = []
    for name, link in all_officials_set:
        res.append(name)
        
    return name
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
