from Tokenize.document import Document
class QueryRanker:
    def __init__(self, docIndex, index):
        self.docIndex = docIndex
        self.index = index
        self.rankIndex = {}
    
    def __calc_TFIDF(self, document, frequency, resourceAppears):
        totalTokens = document.wordCount
        resourceCount = len(self.index)
        weight = (frequency/totalTokens) * (resourceCount/resourceAppears)
        return weight
    def getRanks(self, keyList):
        keyListLength = len(keyList)
        for key in keyList:
            document = self.docIndex[key]
            frequency = self.index[key]
            documentID = document.id
            rank = self.__calc_TFIDF(document, frequency, keyListLength)
            self.rankIndex[documentID] = rank
        self.rankIndex = dict(sorted(self.rankIndex.items(),key=lambda item: item[1],reverse=True))
        return self.rankIndex.keys()
            







        