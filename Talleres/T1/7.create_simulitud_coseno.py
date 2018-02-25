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

inv_frec_vector = []
file_inv_frec_vector = open("inv_frec_vector.txt", "r")
inv_frec_vector = json.JSONDecoder().decode(file_inv_frec_vector.read())
file_inv_frec_vector.close()

query = "company bahia cocoa usa a e i"
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
for id, ter_frec in enumerate(vectorSpace):
    eq = 0
    if ter_frec > 0:
        eq = ter_frec*inv_frec_vector[id]
    tfidf.append(eq)

# Aca con el index invertido
cosSim = {}
for palabra in histQuery:
    if palabra in inverdIndex:  # si la palabra esta en el index invertido
        for key in inverdIndex.get(palabra):
            if key not in cosSim:
                calc = cosine_similarity(tfidf, allTfidf[key])
                cosSim[key] = calc

print()
print("Tiempo total de la busqueda %0.3fs." % totalTime)
print("Total de documentos encontrados: " + len(docs))
print("La consulta es: " + query)
print()

i = 0
for key in sorted(cosSim, key=cosSim.get, reverse=True):
    print("Documento encontrado: #%s, SimCos: %f" % (i,cosSim[key]))
    print('Doc %s: %s' % (key, documents[key]) + "...")
    print()
    i += 1

    if i>10:
        break
        
