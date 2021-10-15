import constants as constant
import nltk
from nltk.stem import PorterStemmer
import pickle
from Tokenize.tokenizer import Tokenizer

class Identifier:

    def __init__(self, query, index, stop_words):
        self.query = query
        self.documents = {}
        self.index = index
        self.stop_words = stop_words

    def filter_query(self):
        ps = PorterStemmer()
        tokenizer = Tokenizer()
        self.query = tokenizer.clean_line(self.query)
        tokens = nltk.word_tokenize(self.query)
        for word in tokens:
            word = word.lower()
            if word not in self.stop_words:
                word = ps.stem(word)
                if self.index.get(word):
                    for doc in self.index[word]:
                        if self.documents.get(doc):
                            self.documents[doc] += 1
                        else:
                            self.documents[doc] = 1
                else:
                    print(word + " not found in index.")
        sorted_documents = sorted(self.documents, key=lambda k: (self.documents[k]), reverse=True)
        max_val = 0
        top_docs = []
        for doc in sorted_documents:
            if self.documents[doc] >= max_val or len(top_docs) < 50:
                max_val = self.documents[doc]
                top_docs.append(doc)
            else:
                break
        return top_docs