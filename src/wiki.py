from numpy import diff, where
import wikipedia
import requests
from datetime import date, datetime

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def clean_up_res(res):
    return res[res.find("=")+1:].replace("[", "").replace("]", "").replace('"', "").strip()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def parse(d, word, count, s, break_point):
    index = s.find(word+count)

    where_to_stop = len(word+count) + index

    while s[where_to_stop] != break_point:
        where_to_stop += 1

    res = s[index+len(word): where_to_stop]

    if not res and word != "term_start":
        print(word)
        print(s)
        raise Exception("Pattern mismatch.")

    else:
        d[word.strip()] = clean_up_res(res)

    return d
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def terms(s):
    d = {}

    jr = "jr/sr"
    term_start = "term_start"
    term_end = "term_end"
    state = "state"
    count = ""

    if s[s.find(jr) + len(jr): s.find(jr) + len(jr)+1].isdigit():
        count = s[s.find(jr) + len(jr): s.find(jr) + len(jr)+1]

    d = parse(d, jr, count, s, "|")
    d = parse(d, term_start, count, s, "|")
    d = parse(d, term_end, count, s, "|")
    d = parse(d, state, count, s, "|")

    return d
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def go_shopping(l, s, d):
    try:

        while l:

            w = l.pop()
            i = s.find(w)

            # Corner Case
            if "state " == w:
                if s.find("enator from") > 0:
                    leftover = s[s.find("enator from") - 1:]
                    d[w.strip()] = leftover[leftover.find(
                        "from")+5:leftover.find("}}")]
                    continue
                if s.find("state ") == -1 and s.find("state1") > 0:
                    l.append("state1")
                    continue

            if i == -1:
                continue

            else:
                where_to_stop = len(w) + i

                # Corner case
                if w == "birth_date ":
                    while s[where_to_stop] != "}":
                        where_to_stop += 1

                elif w == "alma_mater ":
                    while s[where_to_stop] != "\n":
                        where_to_stop += 1

                else:
                    while s[where_to_stop] != "|":
                        where_to_stop += 1

                res = s[i+len(w): where_to_stop]

                # print(res)

                while w[len(w) - 1].isdigit():
                    w = w[:-1]

                # Corner Case
                if w == "birth_date ":
                    d[w.strip()] = res[res.find("|") + 1:]

                else:
                    d[w.strip()] = clean_up_res(res)

        return d

    except Exception as e:
        print(e)
        print(s)
        # return {}
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the number of transactions per person.
# trans_per_person_total={'Max': 5, 'Sam': 20, ...}
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Official:
    def __init__(self, name, jr, state, term_start, term_end, birth_date, birth_place, party, alma_mater, education):
        self.name = name
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

    def all(self):
        print("self.name")
        print(self.name)
        print("self.jr")
        print(self.jr)
        print("self.state")
        print(self.state)

        print("self.term_end")
        print(self.term_end)

        print("self.term_start")
        print(self.term_start)

        print("self.birth_date")
        print(self.birth_date)

        print("self.birth_place")
        print(self.birth_place)

        print("self.party")
        print(self.party)

        print("self.education")
        print(self.education)

        raise Exception("I'm heartbroken </3.")

    def debug(self):
        if not self.name:
            self.all()

        # if not self.jr:
        #     self.all()

        if not self.state:

            self.all()

        if not self.term_start:
            self.all()

        if not self.birth_place:

            self.all()

        if not self.party:
            self.all()

        if not self.education:
            self.all()

        if not self.birth_date:
            self.all()

        if not self.get_num_of_years():
            self.all()

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
        try:
            term_start = datetime.strptime(self.term_start, '%B %d, %Y').date()
        except:
            self.all()
        diff = today.year - term_start.year
        return diff if diff != 0 else 1
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def page(probable_result_title):
    htmled_tltle = probable_result_title.replace(" ", "%20")

    resp = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={person}&rvsection=0'.format(person=htmled_tltle)).json()

    page_one = next(iter(resp['query']['pages'].values()))
    revisions = page_one.get('revisions', [])

    s = list(revisions[0].values())[2]
    return s
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# https://stackoverflow.com/questions/7638402/how-can-i-get-the-infobox-from-a-wikipedia-article-by-the-mediawiki-api
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def wiki_search(name):

    results = wikipedia.search(name)
    at = 0
    s = ""
    while "politician" not in s:
        s = page(results[at])
        at += 1

    d = terms(s)

    d = go_shopping(["name ", "birth_place ", "party ",
                     "alma_mater ", "education ", "birth_date "], s, d)

    search_name = d.get("name", None)
    jr = d.get("jr/sr", None)
    birth_place = d.get("birth_place", None)
    party = d.get("party", None)
    alma_mater = d.get("alma_mater", None)
    education = d.get("education", None)
    birth_date = d.get("birth_date", None)
    term_start = d.get("term_start", None)
    term_end = d.get("term_end", None)
    state = d.get("state", None)

    x = Official(search_name, jr, state, term_start, term_end,
                 birth_date, birth_place, party, alma_mater, education)

    x.debug()

    return x
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
