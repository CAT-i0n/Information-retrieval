from .managers.DocumentManager import DocumentManager
from nltk.corpus import stopwords
import pymorphy3
from collections import Counter
class Searcher:
    def __init__(self):
        self.manager = DocumentManager()

    def search(query: str):
        pass