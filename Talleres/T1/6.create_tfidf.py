import sys
import json
import pandas as pd
import math
from time import time


def main(args):

    vector_space = {}
    file_list_word = open("vector_space.txt", "r")
    vector_space = json.JSONDecoder().decode(file_list_word.read())

    t0 = time()

    tfidf = {}
    doc_lenght = len(vector_space)
    panda = pd.DataFrame(vector_space)
    
    for key, value in vector_space.items():
        newtable = []
        for ter in value:
            eq = 0
            if ter > 0:                            
                den = (panda[key] > 0).sum()
                if den > 0:
                    eq = ter*math.log(doc_lenght/den)                
            newtable.append(eq)
        tfidf[key] = newtable
    
    print("done in %0.3fs." % (time() - t0))

    file = open("tfidf.txt","w")
    file.write(json.JSONEncoder().encode(tfidf))
    file.close()



# metodo main
if __name__ == '__main__':
    main(sys.argv)
