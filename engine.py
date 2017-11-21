from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.stem.snowball import SnowballStemmer
from operator import itemgetter
import requests, json

def reqListArtikel():
        r = requests.get("https://agri.gravicodev.id/map_data/list.json")
        return r

def reqResult(title):
        r = requests.get("https://agri.gravicodev.id/map_data/"+ title +"-result.json")
        return r

def search(query):
    stop_words = get_stop_words('english')
    stopWords = set(stopwords.words('english'))
    wordsFiltered = []
    stemmer = SnowballStemmer("english")

    stop_words.append(",")
    stop_words.append(".")
    stop_words.append("+")

    tokenize_word = word_tokenize(query)

    for w in tokenize_word:
        if w not in stopWords and w not in stop_words:
            wordsFiltered.append(w)

    wordsStemmed = []

    for w in wordsFiltered:
        wordsStemmed.append(stemmer.stem(w))

    queryArr = []

    for w in wordsStemmed:
        if w not in queryArr:
            queryArr.append(w)

    print(queryArr)

    data = reqListArtikel()
    listArticle = data.json()['list']
    queryResult = []
    
    for x in range(0,len(listArticle)):
        namafile = listArticle[x]
        result = reqResult(namafile)
        result = result.json()
        tmp_score = 0
        for y in range(0,len(queryArr)):
            if queryArr[y] in result["index"]:
                tmp_score += result["counter"][result["index"][queryArr[y]]][1]
        queryResult.append([namafile,tmp_score])
    
    queryResult.sort(key=itemgetter(1),reverse=True)
    return queryResult