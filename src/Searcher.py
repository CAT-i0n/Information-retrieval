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
        query_words_nums = np.where(query_tf_idf>0)[0]


        doc_key_words = []
        doc_key_sent = []
        for doc in documents:
            key_words = []
            
            
            for i in query_words_nums:
                if doc.tf_idf[i]!=0:
                    key_words.append(list(self.manager.vocab.keys())[i])
            
            key_sents = []
            if len(key_words)>0:
                doc_key_words.append(key_words)
                dist.append(scipy.spatial.distance.cosine(query_tf_idf, doc.tf_idf))
                doc = open(self.manager.data_dir+doc.title+".fb2", "r").read()
                sents = re.findall('<p>.+?</p>', doc)[:200]
                parts = []
                for i in sents:
                    for j in i[3:-4].split("."):
                        parts.append(j)
                sents = parts
                for i in sents:
                    sent = re.sub('<.+?>|[^А-яЁё]', ' ', i.lower())
                    words = sent.split(" ")
                    for word in key_words:
                        if word in words:
                            key_sents.append(i)
            doc_key_sent.append(key_sents)
                            

                    
                
                

        closest_docs_nums = np.argsort(dist)

        closest_docs = []

        for i in closest_docs_nums:
            closest_docs.append((documents[i], doc_key_words[i], doc_key_sent[i]))

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
