from __future__ import print_function
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer
from operator import itemgetter
import requests, json, codecs

def reqListArtikel():
    r = requests.get("https://agri.gravicodev.com/map_data/list.json")
    return r

def getArtikelData(artikelname):
    r = requests.get("https://agri.gravicodev.com/map_data/"+ artikelname +".txt");

    return r

stop_words = get_stop_words('english')
stopWords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

stop_words.append(",")
stop_words.append(".")
stop_words.append("+")

data = reqListArtikel()
arrFile = data.json()['list']

for x in range(0,len(arrFile)):
    wordsFiltered = []
    namafile = arrFile[x]
    artikel = getArtikelData(namafile)
    artikel = artikel.text

    tokenize_word = word_tokenize(artikel)

    for w in tokenize_word:
        if w not in stopWords and w not in stop_words:
            wordsFiltered.append(w)

    wordsStemmed = []

    for w in wordsFiltered:
        wordsStemmed.append(stemmer.stem(w))

    counterObj = {}
    counterArr = []

    for w in wordsStemmed:
        if w not in counterArr:
            counterArr.append(w)
            counterObj[w] = 1
        else:
            counterObj[w] += 1

    tmp = []
    for w in counterArr:
        tmp.append([''+w,counterObj[w]])
    tmp.sort(key=itemgetter(1),reverse=True)

    for w in range(0,len(tmp)):
        counterObj[tmp[w][0]] = w

    result = {}
    result['index'] = counterObj
    result['counter']= tmp

    result = json.dumps(result)
    file = open(namafile+'-result.json', 'w')
    file.write(result)
    file.close()