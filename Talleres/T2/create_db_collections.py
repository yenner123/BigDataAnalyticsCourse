from pymongo import MongoClient
from json import JSONDecoder

def opendDocuments():    
    file_inverdIndex = open("inverdIndex.txt", "r")
    inverdIndex = JSONDecoder().decode(file_inverdIndex.read())
    file_inverdIndex.close()
    
    file_stopwords = open("stopwords.txt", "r", errors="replace")
    stopwords = file_stopwords.read().split()
    file_stopwords.close()
    
    file_words = open("words.txt", "r")
    words = JSONDecoder().decode(file_words.read())
    file_words.close()
    
    file_words = open("tfidf.txt", "r")
    allTfidf = JSONDecoder().decode(file_words.read())
    file_words.close()

    file_documents = open("documents.txt", "r")
    documents = JSONDecoder().decode(file_documents.read())
    file_documents.close()

    file_inv_frec_vector = open("inv_frec_vector.txt", "r")
    inv_frec_vector = JSONDecoder().decode(file_inv_frec_vector.read())
    file_inv_frec_vector.close()
    
    return inverdIndex, stopwords, words, allTfidf, documents, inv_frec_vector

## main
client = MongoClient()
db = client.text

## abrir documentos con los documentos procesados
inverdIndex, stopwords, words, allTfidf ,documents, inv_frec_vector = opendDocuments()

## Add inverd index
dbInverdIndex = db.inverdIndex
dbInverdIndex.delete_many({})
i = 0
for key,value in inverdIndex.items():
    dic = {}
    dic ['_id'] = i
    dic ['word'] = key
    dic ['docs'] = value
    i+=1
    dbInverdIndex.insert_one(dic)
print("added inverd_index collection")

## Add stopwords
dbStopwords = db.stopwords
dbStopwords.delete_many({})
for id, stopword in enumerate(stopwords):
    dic = {}
    dic ['_id'] = id
    dic ['stopword'] = stopword    
    i+=1
    dbStopwords.insert_one(dic)
print("added stopwords collection")

## Add words
dbWords = db.words
dbWords.delete_many({})
for id, word in enumerate(words):   
    dic = {}
    dic ['_id'] = id
    dic ['words'] = word        
    dbWords.insert_one(dic)
print("added words collection")

## Add allTfidf
dbAllTfidf = db.allTfidf
dbAllTfidf.delete_many({})
i = 0
for key,value in allTfidf.items():
    dic = {}
    dic ['_id'] = i
    dic ['doc'] = key
    dic ['words'] = value
    i+=1
    dbAllTfidf.insert_one(dic)
print("added allTfidf collection")

## Add documents
dbDocuments = db.documents
dbDocuments.delete_many({})
i = 0
for key,value in documents.items():
    dic = {}
    dic ['_id'] = key
    dic ['doc'] = value    
    i+=1
    dbDocuments.insert_one(dic)
print("added documents collection")

## Add inv_frec_vector
dbInv_frec_vector= db.inv_frec_vector
dbInv_frec_vector.delete_many({})
for id,value in enumerate(inv_frec_vector):
    dic = {}
    dic ['_id'] = id
    dic ['value'] = value        
    dbInv_frec_vector.insert_one(dic)
print("added inverse frecuency vector collection")

print("finish")