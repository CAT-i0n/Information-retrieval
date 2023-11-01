from .managers.DocumentManager import DocumentManager
from nltk.corpus import stopwords
import pymorphy3
from collections import Counter
import re
import numpy as np
import scipy

class Searcher:
    def __init__(self):
        self.manager = DocumentManager()

    def search(self, query: str):        
        query_tf_idf = self.get_query_vector(query)
        if query_tf_idf is None:
            return []
        documents = self.manager.get_documents()
        dist = []

        for doc in documents:
            dist.append(scipy.spatial.distance.cosine(query_tf_idf, doc.tf_idf))

        closest_docs_nums = np.argsort(dist)[:5]

        closest_docs = []

        for i in closest_docs_nums:
            closest_docs.append(documents[i].title)
        
        print(closest_docs)
        return closest_docs
        
        
    def get_query_vector(self, query):
        query = re.sub('<.+?>|[^А-яЁё]', ' ', query.lower())
        words = query.split(" ")

        
        stopWords = stopwords.words("russian") + ['']

        morph = pymorphy3.MorphAnalyzer()
        words = [morph.parse(i)[0].normal_form for i in words if i not in stopWords]
        words_size = len(words)
        if words_size == 0:
            return None
        bug = Counter(words)
        print(len(self.manager.vocab))
        tf_idf = np.zeros((len(self.manager.vocab)))
        for i, word in enumerate(self.manager.vocab):
            tf_idf[i] = self.manager.idf[word]*bug[word]/words_size
        
        return tf_idf
    
    def cos_dist(self, vec1, vec2):
        pass