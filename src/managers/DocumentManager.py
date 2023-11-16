import re
from nltk.corpus import stopwords
import pymorphy3
from collections import Counter
import os
from math import log
import numpy as np
from tqdm import tqdm
import couchdb

class Document:
    def __init__(self, title, file):
        self.title: str = title[:-4]
        self.author: str = ""
        self.tf_idf = []
        self.words_num = 0
        self.text = file.read().decode()
        self.__set_author(self.text)

    def process_document(self, sent_num = 1000) -> list:
        sents = re.findall('<p>.+?</p>', self.text)[:sent_num]
        text = "".join(sents)
        text = re.sub('<.+?>|[^А-яЁё]', ' ', text.lower())

        words = text.split(" ")
        self.words = self.__normalize_text(words)

    def __set_author(self, book):
        
        author_pos_start = re.search('<first-name>', book)
        author_pos_end = re.search('</first-name>', book)

        self.author += book[author_pos_start.end():author_pos_end.start()]
        
        author_pos_start = re.search('<last-name>', book)
        author_pos_end = re.search('</last-name>', book)
        
        self.author += " " + book[author_pos_start.end():author_pos_end.start()]

        #print(self.author)

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

        server = couchdb.Server("http://admin:12345\@localhost:5984")
        server.resource.credentials = ('admin', '12345')
        self.db = server['books']
        self.load_documents()
        # self.compute_idf()
        # self.index_documents()

    def update_docs(self):
        for id in self.db:
            self.db.delete(self.db[id])
        
        for book in tqdm(os.listdir(self.data_dir)):
            self.db[book] = {}
            file = open(self.data_dir+book)
            self.db.put_attachment(self.db[book], file, filename=book)
        
        self.documents = []
        for id in tqdm(self.db):
            if id == 'data':
                continue
            file = self.db.get_attachment(self.db[id], id)
            doc = Document(id, file)
            doc.process_document()
            words = doc.words
            for word in words:
                self.vocab[word] = self.vocab.get(word, 0) + 1
            self.documents.append(doc)

        self.size = len(self.documents)
        self.norm_size = self.size**0.5

        self.compute_idf()
        self.index_documents()

        self.db['data'] = {'vocab' : self.vocab, 'idf': self.idf}

        for doc in self.documents:
            db_doc = self.db[doc.title + '.fb2']
            db_doc['tf'] = doc.tf_idf.tolist()
            self.db.update([db_doc])

        

        

    def load_documents(self):
        try:
            for id in self.db:
                if id == 'data':
                    continue
                file = self.db.get_attachment(self.db[id], id)
                print(file)
                doc = Document(id, file)

                doc.tf_idf = self.db[id]['tf']
                self.documents.append(doc)
            self.size = len(self.documents)
            self.norm_size = self.size**0.5
            self.vocab = self.db['data']['vocab']
            self.idf = self.db['data']['idf']
        except:
            self.update_docs()

    def compute_idf(self):
        for word in self.vocab:
            self.idf[word] = (log(self.size/self.vocab[word])+1)/self.norm_size


    def index_documents(self):
        for doc in self.documents:
            tf_idf = np.zeros((len(self.vocab)))
            for i, word in enumerate(self.vocab):
                tf_idf[i] = self.idf[word]*doc.words[word]/doc.words_num
            doc.tf_idf = tf_idf

    def get_documents(self):
        return self.documents
