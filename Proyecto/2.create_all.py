import sys
import json
from time import time
from math import log
from collections import Counter

def RemoveSymbols(word):    
    word = word.replace("==", " ")
    word = word.replace("(", " ")
    word = word.replace(")", " ")
    word = word.replace(".", " ")
    word = word.replace(",", " ")
    word = word.replace(" =", " ")
    word = word.replace("\n", " ")
    word = word.replace("\r", " ")
    word = word.replace("\t", " ")
    word = word.replace(":", " ")
    word = word.replace("*", " ")
    word = word.replace("[", " ")
    word = word.replace("]", " ")
    word = word.replace(">", " ")
    word = word.replace("<", " ")
    word = word.replace('"\"', ' ')
    word = word.replace("/", " ")
    word = word.replace("«", " ")
    word = word.replace("»", " ")
    word = word.replace("—", " ")
    word = word.replace("     ", " ")
    word = word.replace("    ", " ")
    word = word.replace("   ", " ")
    word = word.replace("  ", " ") 
    word = word.replace(' "', " ") 
    word = word.replace('" ', " ") 
    word = word.replace(' " ', " ") 
    word = word.replace('""', " ") 
    word = word.replace('" "', " ") 
    word = word.replace(' "" ', " ") 
    word = word.replace('\u200b', " ") 
    return word

def isNotEmpty(s):
    return bool(s and s.strip())

def main(args):
    stopwords = []
    file_stopwords = open("spanish.txt", "r", encoding='utf-8')
    stopwords = file_stopwords.read().split()

    corpus = {}
    file_documents = open("corpus.txt", "r", encoding='utf-8')
    corpus = json.JSONDecoder().decode(file_documents.read())

    t0 = time()

    dataset = {}
    dictionary = []
    inverterIndex = {}
    tfidf = {}    
    inv_frec_vector = []

    for key, doc in corpus.items():
        doc_listwords = []
        for word in RemoveSymbols(doc.lower()).split():                                     
            if word not in stopwords and isNotEmpty(word):                
                doc_listwords.append(word)                 
                if word in inverterIndex:                
                    if key not in inverterIndex[word]:
                        inverterIndex[word].append(key)
                else:
                    inverterIndex[word] = [key]              
        dataset[key] = Counter(doc_listwords)
    
    doc_lenght = len(dataset)
    
    for word, docs in inverterIndex.items():                                                            
        inv_frec = log(doc_lenght/len(docs))               
        for doc_id, doc_words in dataset.items():     
            eq = doc_words.get(word, 0)*inv_frec            
            if doc_id in tfidf:                                
                tfidf[doc_id].append(eq) 
            else:
                tfidf[doc_id] = [eq] 
        inv_frec_vector.append(inv_frec)    
    
    print("done in %0.3fs." % (time() - t0))

    dictionary =  list(inverterIndex.keys())    

    with open('dataset.txt', 'w', encoding='utf-8') as file:
        json.dump(dataset, file, ensure_ascii=False)

    with open('dictionary.txt', 'w', encoding='utf-8') as file:        
        json.dump(dictionary, file, ensure_ascii=False)

    with open('inverterIndex.txt', 'w', encoding='utf-8') as file:
        json.dump(inverterIndex, file, ensure_ascii=False)

    with open('inv_frec_vector.txt', 'w', encoding='utf-8') as file:
        json.dump(inv_frec_vector, file, ensure_ascii=False)

    with open('tfidf.txt', 'w', encoding='utf-8') as file:
        json.dump(tfidf, file, ensure_ascii=False)

    print("finish")
    
# metodo main
if __name__ == '__main__':
    main(sys.argv)
    