# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions per person.
# trans_per_person_total={'Max': 5, 'Sam': 20, ...}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Representative: 
    def __init__(self, name, jr, state, term_start, birth_place, party, alma_mater, education):
        self.name = name
        self.jr = jr 
        self.state = state
        self.term_state = term_start
        self.birth_place = birth_place
        self.party = party
        if alma_mater:
            self.education = alma_mater
        else:
            self.education = education
    
    def name(self):
        return self.name
    
    def jr(self):
        return self.jr

    def state(self):
        return self.state

    def term_state(self):
        return self.term_state

    def birth_place(self):
        return self.birth_place

    def party(self):
        return self.party

    def education(self):
        return self.education
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
