import sys
import json
from time import time
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
    word = word.replace("\"", " ")
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

    dataset = {}
    file_documents = open("corpus.txt", "r", encoding='utf-8')
    dataset = json.JSONDecoder().decode(file_documents.read())

    t0 = time()

    newDoc = {}
    dictionary = []
    inverterIndex = {}
    for key, doc in dataset.items():
        doc_listwords = []
        for word in RemoveSymbols(doc.lower()).split():                                     
            if word not in stopwords and isNotEmpty(word):
                doc_listwords.append(word) 
                
                if word in inverterIndex:                
                    if key not in inverterIndex[word]:
                        inverterIndex[word].append(key)
                else:
                    inverterIndex[word] = [key]

                if word not in dictionary:
                    dictionary.append(word)
        newDoc[key] = Counter(doc_listwords)

    print("done in %0.3fs." % (time() - t0))
   
    with open('dataset.txt', 'w', encoding='utf-8') as file:
        json.dump(newDoc, file, ensure_ascii=False)

    with open('dictionary.txt', 'w', encoding='utf-8') as file:        
        json.dump(dictionary, file, ensure_ascii=False)

    with open('inverterIndex.txt', 'w', encoding='utf-8') as file:
        json.dump(inverterIndex, file, ensure_ascii=False)

# metodo main
if __name__ == '__main__':
    main(sys.argv)