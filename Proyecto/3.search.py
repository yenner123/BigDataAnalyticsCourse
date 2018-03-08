#%%

import json
import utils
from time import time
from collections import Counter

def opendDocuments():
    file_inverdIndex = open("inverterIndex.txt", "r", encoding='utf-8')
    inverdIndex = json.JSONDecoder().decode(file_inverdIndex.read())
    file_inverdIndex.close()

    file_stopwords = open("spanish.txt", "r", encoding='utf-8')
    stopwords = file_stopwords.read().split()
    file_stopwords.close()

    file_words = open("tfidf.txt", "r", encoding='utf-8')
    allTfidf = json.JSONDecoder().decode(file_words.read())
    file_words.close()

    file_documents = open("corpus.txt", "r", encoding='utf-8')
    corpus = json.JSONDecoder().decode(file_documents.read())
    file_documents.close()

    file_inv_frec_vector = open("inv_frec_vector.txt", "r", encoding='utf-8')
    inv_frec_vector = json.JSONDecoder().decode(file_inv_frec_vector.read())
    file_inv_frec_vector.close()

    return inverdIndex, stopwords, allTfidf, corpus, inv_frec_vector

def search(query):
    dataset = {}        
    tfidf = []       
    cos_sim = {}

    doc_listwords = []
    for word in utils.removeSymbols(query.lower()).split():                                     
        if word not in stopwords and utils.isNotEmpty(word):                
            doc_listwords.append(word)                                        
    dataset = Counter(doc_listwords)
    
    for id, word in enumerate(inverdIndex.keys()):                                                                        
        eq = 0
        if word in dataset:
            eq = dataset.get(word, 0)*inv_frec_vector[id]
        tfidf.append(eq)       
    
    for word in dataset.keys():
        if word in inverdIndex:  # si la palabra esta en el index invertido
            for key in inverdIndex.get(word):
                if key not in cos_sim:
                    calc = utils.cosineSimilarity(tfidf, allTfidf[key])
                    cos_sim[key] = calc
    return cos_sim    

""" main """
# abrir documentos con los documentos procesados
inverdIndex, stopwords, allTfidf, corpus, inv_frec_vector = opendDocuments()

query = "query"

# obtiene el tiempo actual
t0 = time()

# realiza la consulta
docs = search(query)

# obtiene el tiempo total de la busqueda
totalTime = time()-t0

# muestra resultados
print()
print("Tiempo total de la busqueda %0.3fs." % totalTime)
print("Total de documentos encontrados: %d" % len(docs))
print("La consulta es: " + query)
print()

i = 0
for key in sorted(docs, key=docs.get, reverse=True):
    print("Documento encontrado: #%s, cs: %f" % (i, docs[key]))
    print('Documento #%s: %s' % (key, corpus[key]))
    print()
    i += 1

    if (i > 10):
        break
