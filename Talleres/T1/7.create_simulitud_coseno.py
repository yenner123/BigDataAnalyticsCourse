import math
import json
from time import time
from collections import Counter
from nltk.tokenize import word_tokenize

def find(doc, find_term):
    coincidences = 0
    for word in doc:
        if word == find_term:
            coincidences = coincidences + 1
    return coincidences


def cosine_similarity(vectorSpace1, vectorSpace2):
    numerator = 0 
    sumxx, sumyy = 0, 0
    for i in range(len(vectorSpace1)):
        x = vectorSpace1[i]
        y = vectorSpace2[i]
        sumxx += x*x
        sumyy += y*y
        numerator += x*y
    return numerator/math.sqrt(sumxx*sumyy)


inverdIndex = {}
file_inverdIndex = open("inverdIndex.txt", "r")
inverdIndex = json.JSONDecoder().decode(file_inverdIndex.read())
file_inverdIndex.close()

stopwords = []
file_stopwords = open("stopwords.txt", "r", errors="replace")
stopwords = file_stopwords.read().split()
file_stopwords.close()

words = []
file_words = open("words.txt", "r")
words = json.JSONDecoder().decode(file_words.read())
file_words.close()

allTfidf = {}
file_words = open("tfidf.txt", "r")
allTfidf = json.JSONDecoder().decode(file_words.read())
file_words.close()

documents = {}
file_documents = open("documents.txt", "r")
documents = json.JSONDecoder().decode(file_documents.read())
file_documents.close()

query = "USA"
t0 = time()

listQuery = []
for word in word_tokenize(query.lower()):  # split
    if word not in stopwords:
        listQuery.append(word)

histQuery = Counter(listQuery)

vectorSpace = []
for word in words:
    vectorSpace.append(find(histQuery, word))

tfidf = []
doc_lenght = len(vectorSpace)
for ter in vectorSpace:
    eq = 0
    if ter > 0:
        eq = ter*math.log(doc_lenght)
    tfidf.append(eq)

# Aca con el index invertido
cosSim = {}
for palabra in histQuery:
    if palabra in inverdIndex:  # si la palabra esta en el index invertido
        for key in inverdIndex.get(palabra):
            if key not in cosSim:
                calc = cosine_similarity(tfidf, allTfidf[key])
                cosSim[key] = calc


print("done in %0.3fs." % (time() - t0))

# print(cosSim)

print("Query is: " + query)
print()

i = 0
for key in sorted(cosSim, key=cosSim.get):
    print("Topic #%s:" % i)
    print('%.300s' % documents[key] + "...")
    print()
    i += 1
