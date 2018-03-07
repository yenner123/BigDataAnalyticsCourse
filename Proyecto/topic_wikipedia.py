#%%
from __future__ import print_function
from json import JSONDecoder
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.datasets import fetch_20newsgroups

n_samples = 500
n_features = 500
n_topics = 10
n_top_words = 30

t0 = time()
print("Loading dataset and extracting TF-IDF features...")

file_stopwords = open("spanish.txt", "r", encoding='utf-8')
stopwords = file_stopwords.read().split()
file_stopwords.close()

f = open('corpus.txt', 'r')
corpus = JSONDecoder().decode(f.read())
f.close()

dataset = []
for documents in corpus.values():        
    dataset.append(documents.lower())        

vectorizer = TfidfVectorizer(
    max_df=0.95, min_df=2, max_features=n_features, stop_words=stopwords)

tfidf = vectorizer.fit_transform(dataset[:n_samples])

print("done in %0.3fs." % (time() - t0))
print()

print("Fitting the NMF model with n_samples=%d and n_features=%d..." %
      (n_samples, n_features))

nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)

print("done in %0.3fs." % (time() - t0))

feature_names = vectorizer.get_feature_names()

print()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
