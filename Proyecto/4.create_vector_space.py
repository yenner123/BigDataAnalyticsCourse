import sys
import json

def find(doc, find_term):
    coincidences = 0
    for word in doc:
        if word == find_term:
            coincidences = coincidences + 1
    return coincidences


def main(args):
    words = []
    file_words = open("dictionary.txt", "r", encoding='utf-8')
    words = json.JSONDecoder().decode(file_words.read())

    documents = {}
    file_documents = open("dataset.txt", "r", encoding='utf-8')
    documents = json.JSONDecoder().decode(file_documents.read())

    listword = {}
    for key, doc in documents.items():
        hist = []
        for word in words:
            hist.append(find(doc, word))
        listword[key] = hist

    with open('vector_space.txt', 'w', encoding='utf-8') as file:
        json.dump(listword, file, ensure_ascii=False)

# metodo main
if __name__ == '__main__':
    main(sys.argv)
