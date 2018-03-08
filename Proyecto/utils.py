import math

def removeSymbols(word):    
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

def cosineSimilarity(vectorSpace1, vectorSpace2):
    numerator = 0
    sumxx, sumyy = 0, 0
    for i in range(len(vectorSpace1)):
        x = vectorSpace1[i]
        y = vectorSpace2[i]
        sumxx += x*x
        sumyy += y*y
        numerator += x*y
    return numerator/math.sqrt(sumxx*sumyy)
