import sys
import json
from time import time

def createTweetDict(docs):
    inverterIndex = {}
    for key, text in docs.items():
        for word in text:            
            if inverterIndex.get(word, False):
                if key not in inverterIndex[word]:
                    inverterIndex[word].append(key)
            else:
                inverterIndex[word] = [key]
    return inverterIndex


def main(args):

    vector_space = {}
    file_list_word = open("doc_wt_sw.txt", "r")
    vector_space = json.JSONDecoder().decode(file_list_word.read())

    t0 = time()

    inverdIndex = createTweetDict(vector_space)

    print("done in %0.3fs." % (time() - t0))

    file = open("inverdIndex.txt", "w")
    file.write(json.JSONEncoder().encode(inverdIndex))
    file.close()

# metodo main
if __name__ == '__main__':
    main(sys.argv)
