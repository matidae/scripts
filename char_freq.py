import urllib, json, re, random, string

word = "Book"
langs = ['cs', 'da', 'de', 'en', 'es', 'eu', 'fi', 'fr', 'hu', 'is', 'it', 'la', 'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv']

def get_interlangs(word, langs):
    dict_langs = {}
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&titles=" + word + "&props=labels&format=json"
    response = urllib.urlopen(url)
    jsonlang = json.load(response)
    key = ""
    for k in jsonlang['entities']:
        key = k
        break
    labels = jsonlang['entities'][key]['labels']
    for i in labels:
        if i in langs:
            dict_langs[i] = labels[i]['value']
    return dict_langs

dict_langs = get_interlangs(word, langs)

def get_some_words(word, lang):
    urltext = "https://" + lang + ".wikipedia.org/w/api.php?action=query&prop=revisions&titles=" + word + "&rvprop=content&format=json"
    response_text = urllib.urlopen(urltext)
    json_text = json.load(response_text)
    for k in json_text['query']['pages']:
        key = str(k)
        break
    text  = json_text['query']['pages'][key]['revisions']
    list_text =  str(text).split()
    filter_text = []
    for word in list_text:
        if len(word)>3 and re.match('^[a-z]*$', word.lower()):
            filter_text.append(word.lower())
    return random.sample(set(filter_text), 10)

dict_words = {}
for l in langs:
    if l in dict_langs.keys():
        word_lang = dict_langs[l]
        word_list = get_some_words(word_lang.encode("utf-8"), l)
        dict_words[l] = word_list
print  dict_words

char_dict = {i:0 for i in string.ascii_lowercase}
from itertools import permutations
l = list(string.ascii_lowercase * 1)
kwords = []
for i in sorted(set(permutations(l,1))):
    kwords.append("".join(i))




