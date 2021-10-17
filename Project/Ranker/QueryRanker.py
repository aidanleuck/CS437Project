from Tokenize.document import Document
import constants as constant
import pickle
import Global as globals

import constants as constant
import nltk
from nltk.stem import PorterStemmer
from Tokenize.tokenizer import Tokenizer

class QueryRanker:
    def __init__(self, query, index, stop_words):
        self.query = query
        with open(constant.DOC_PATH, 'rb') as i:
            self.docIndex = pickle.load(i)
        self.index = index
        self.stop_words = stop_words
        self.rankIndex = {}
    def getRanks(self, keyList):
        s = PorterStemmer()
        tokenizer = Tokenizer()
        for key in keyList:
            frequency = 0
            rank = 0
            document = self.docIndex[key]
            self.query = tokenizer.clean_line(self.query)
            tokens = nltk.word_tokenize(self.query)
            for word in tokens:
                word = word.lower()
                if word not in self.stop_words:
                    word = s.stem(word)
                    documentList = self.index.get(word)
                    value = documentList.get(document.id)
                    if(value is not None):
                        frequency = documentList.get(document.id)
                        numberOfDocs = len(documentList)
                        totalTokens = document.word_count
                        resourceCount = len(self.docIndex)
                        rank += globals.calc_TFIDF(frequency, totalTokens, resourceCount, numberOfDocs)
            self.rankIndex[document] = rank
        self.rankIndex = dict(sorted(self.rankIndex.items(),key=lambda item: item[1],reverse=True))
        return list(self.rankIndex.keys())