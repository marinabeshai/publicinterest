class Congress:
    
    def __init__(self, number, num_of_senators,  senate_party, senate_members, num_of_representatives, house_party, house_members):
        self.number = number 
        self.num_of_senators = num_of_senators
        self.senate_party = senate_party
        self.senate_members = senate_members
        self.num_of_representatives = num_of_representatives
        self.house_party = house_party
        self.house_members = house_members
        
    def debug(self):
        return(
            "self.number :{}\n num_of_senators: {}\n senate_party: {}\nsenate_members: {}\nnum_of_representatives: {}\nhouse_party: {}\nhouse_members: {}".format(self.number, self.num_of_senators, self.senate_party, self.senate_members, self.num_of_representatives, self.house_party, self.house_members)
        )


    
    
    