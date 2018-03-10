import wikipedia
import json
from time import sleep


corpus = {}
n_len = 500

wikipedia.set_rate_limiting(False)
wikipedia.set_lang("es")
pagesList = wikipedia.random(n_len) + wikipedia.random(n_len)
print(len(pagesList))

for i, page in enumerate(pagesList):
    print("Processing page...", end=' ')
    try:
        foundPage = wikipedia.page(page)
    except:
        corpus[i] = ""
        print("page %i is void" % i)
        continue

    corpus[i] = foundPage.title + " " + foundPage.content
    print("page %i added" % i)
    # sleep(0.1)  # evita ser bloquedo por multiples peticiones

print("Finish")

with open('corpus.txt', 'w', encoding='utf-8') as file:
    json.dump(corpus, file, ensure_ascii=False)
