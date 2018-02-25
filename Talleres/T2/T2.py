# ## TallerNro1:  Buscador de texto por palabras claves usando VSM y Similitud Coseno
# ### Autores: Yenner Robayo, Wilmar Martín

import json
import math
from collections import Counter
from time import time
from pymongo import MongoClient

def readDatabase(db):
    inverdIndex = db.inverdIndex
    stopwords = db.stopwords
    words = db.words
    allTfidf = db.allTfidf
    documents = db.documents
    inv_frec_vector = db.inv_frec_vector

    return inverdIndex, stopwords, words, allTfidf, documents, inv_frec_vector


def findCoincidences(doc, find_term):
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


def createHistogram(query):
    listQuery = []
    for word in query.lower().split():  # split              
        if stopwords.find_one({'stopword':  word}) is None:                            
            listQuery.append(word)
    return Counter(listQuery)


def createVectorSpace(histogram):
    vectorSpace = []
    for word in words.find():        
        vectorSpace.append(findCoincidences(histogram, word.get('words')))
    return vectorSpace


def createTdiDf(vectorSpace):
    tfidf = []
    for id, ter_frec in enumerate(vectorSpace):
        eq = 0
        if ter_frec > 0:
            inv_frec = inv_frec_vector.find_one({'_id':  id})
            eq = ter_frec*inv_frec.get('value')
        tfidf.append(eq)
    return tfidf


def search(tfidf):
    cosSim = {}
    for palabra in histQuery:        
        inv_idx = inverdIndex.find_one({'word':  palabra})
        if inv_idx != None:                
            for key in inv_idx.get('docs'):
                if key not in cosSim:
                    documents_tfidf = allTfidf.find_one({'doc': key})
                    calc = cosine_similarity(tfidf, documents_tfidf.get('words'))
                    cosSim[key] = calc
    return cosSim


# Cliente base de
client = MongoClient()
db = client.text

# abrir las colecciones desde la base de datos
inverdIndex, stopwords, words, allTfidf, documents, inv_frec_vector = readDatabase(db)

#consulta
query = input('Ingrese texto a buscar: ')

### Algoritmo de Búsqueda

# obtiene el tiempo actual
t0 = time()

# crea al vector de histograma de la cosulta
histQuery = createHistogram(query)

# crea el vector space de la consulta
vectorSpace = createVectorSpace(histQuery)

# normaliza TF-IDF
tfidf = createTdiDf(vectorSpace)

# realiza la consulta
docs = search(tfidf)

# obtiene el tiempo total de la busqueda
totalTime = time()-t0

# Muestra resultados
print()
print("Tiempo total de la busqueda %0.3fs." % totalTime)
print("Total de documentos encontrados: " + len(docs))
print("La consulta es: " + query)
print()
i = 0
for key in sorted(docs, key=docs.get, reverse=True):
    document = documents.find_one({'_id': key})    
    print("Documento encontrado: #%s" % i)
    print('%s' % document.get('doc') + "...")
    print()
    i += 1

    if (i > 10):
        break
