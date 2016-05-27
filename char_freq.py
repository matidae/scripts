import urllib, json, re, random, string
from itertools import permutations

word = "Book"
sample_size = 150
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

def get_some_words(word, lang, sample_size):
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
        if len(set(filter_text)) >= sample_size:
            return random.sample(set(filter_text), sample_size)

def sample_dict_words(langs, dict_langs, sample_size):
    dict_words = {}
    for l in langs:
        if l in dict_langs.keys():
            word_lang = dict_langs[l]
            word_list = get_some_words(word_lang.encode("utf-8"), l, sample_size)
            dict_words[l] = word_list
    return  dict_words

def generate_kwords(num):
    l = list(string.ascii_lowercase * num)
    kwords = []
    for i in sorted(set(permutations(l, num))):
        kwords.append("".join(i))
    return kwords

def generate_freq_vector(kdict, word_list):
    klist = [0] * len(kdict)
    for word in word_list:
        for char in word:
            klist[kdict[char]] += 1
    return klist

dict_langs = get_interlangs(word, langs)
dict_words = sample_dict_words(langs, dict_langs, sample_size)
kwords= generate_kwords(1)
kdict = {i:k for k,i in enumerate(kwords)}

for k in dict_words:
        if dict_words[k]:
            kvector = generate_freq_vector(kdict, dict_words[k])
            print k +',' + ','.join(map(str, kvector))
        
