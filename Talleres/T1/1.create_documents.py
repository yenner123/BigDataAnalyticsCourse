from bs4 import BeautifulSoup
import glob
import os
import sys
import json
 
def replace(string):    
    string = string.replace("\n", " ")
    string = string.replace("\r", " ")
    string = string.replace("\t", " ")
    string = string.replace("\x03", " ")    
    string = string.replace("     ", " ")
    string = string.replace("    ", " ")
    string = string.replace("   ", " ")
    string = string.replace("  ", " ")    
    return  string
        

def main(args):
    
    path_documents = 'documents/'
    documents = []
    for filename in glob.glob(os.path.join(path_documents, '*.sgm')):
        file = open(filename, "r")        
        documents.append(BeautifulSoup(file.read(), "html.parser"))             

    file = open("documents.txt","w", encoding="utf8")     
    dic = {}    
    count = 0
    for doc in documents:     
        for reuters in doc.find_all('reuters'):       
            title = ""
            body = ""

            if reuters.title:                        
                title = reuters.title.get_text()
            if reuters.body:
                body = reuters.body.get_text()

            content = title + " " + body
            
            dic[count] = replace(content).lower()
            count = count + 1       
                
    file.write(json.JSONEncoder().encode(dic))
    file.close()
    print(count)

# metodo main
if __name__ == '__main__':
    main(sys.argv)

