import re
from nltk.corpus import stopwords
import pymorphy3
from collections import Counter
import os
from math import log
import numpy as np

class Document:
    def __init__(self, title, addr):
        self.title: str = title
        #self.text: str = ""
        self.tf_idf = []
        self.words_num = 0
        self.PASS_SENTENCES = 20
        self.words = self.process_document(addr)

    def process_document(self, addr: str, sent_num = 200) -> list:
        book = open(addr, "r").read()

        sents = re.findall('<p>.+?</p>', book)[:sent_num+self.PASS_SENTENCES]
        text = "".join(sents[self.PASS_SENTENCES:])
        text = re.sub('<.+?>|[^А-яЁё]', ' ', text.lower())

        words = text.split(" ")
        return self.__normalize_text(words)

    def __normalize_text(self, words: list) -> str:
        stopWords = stopwords.words("russian") + ['']
        morph = pymorphy3.MorphAnalyzer()
        words = [morph.parse(i)[0].normal_form for i in words if i not in stopWords]
        self.words_num = len(words)
        return Counter(words)


class DocumentManager:
    def __init__(self):
        self.data_dir = 'data/' 
        self.documents: list = []
        self.vocab = {}
        self.idf = {}
        self.load_documents()
        self.compute_idf()
        self.index_documents()

    def load_documents(self):
        for book in os.listdir(self.data_dir):
            doc = Document(book, self.data_dir+book)
            words = doc.words
            for word in words:
                self.vocab[word] = self.vocab.get(word, 0) + 1
            self.documents.append(doc)
        self.size = len(self.documents)

    def compute_idf(self):
        for word in self.vocab:
            self.idf[word] = log(self.size/self.vocab[word])


    def index_documents(self):
        for doc in self.documents:
            tf_idf = np.zeros((len(self.vocab)))
            for i, word in enumerate(self.vocab):
                tf_idf[i] = self.idf[word]*doc.words[word]/doc.words_num
            doc.tf_idf = tf_idf

    def get_documents(self):
        return self.documents
