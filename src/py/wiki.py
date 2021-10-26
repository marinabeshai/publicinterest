import wikipedia 
import requests
import json
# https://stackoverflow.com/questions/7638402/how-can-i-get-the-infobox-from-a-wikipedia-article-by-the-mediawiki-api


# if __name__ == '__main__':
def wiki_search(name):

    probable_result_title = wikipedia.search(name)[0]
    htmled_tltle = probable_result_title.replace(" ", "%20")


    resp = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={person}&rvsection=0'.format(person=htmled_tltle)).json()
        

    page_one = next(iter(resp['query']['pages'].values()))
    revisions = page_one.get('revisions', [])

    l = ["name", "jr/sr", "state", "birth_place", "party", "alma_mater"]
    d = {}

    s = list(revisions[0].values())[2]

    for w in l:
        i = s.find(w)
        where_to_stop = len(w) + i 
        while s[where_to_stop] != "|":
            where_to_stop += 1 
            
        res = s[i+len(w): where_to_stop]
        d[w] =  res.replace("=", "").replace("[", "").replace("]", "").strip()
        
    print(d)

