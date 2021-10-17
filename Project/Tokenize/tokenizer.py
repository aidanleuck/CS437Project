import nltk
import csv
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import constants as constant
import pickle
from Tokenize.document import Document

class Tokenizer:

    def __init__(self):
        print("Tokenizer initialized")

    def clean_line(self, line):
        # Remove the following punctuation: ,."“/)(\[]{}!?:;'$&% and other random punctuation from strange csv file
        regexPunc = r',|\.|\"|\“|\/|\)|\(|\\|\[|\]|\{|\}|\!|\?|\:|\;|\'|\$|\&|\%|\-|1|2|3|4|5|6|7|8|9|\0'
        return re.sub(regexPunc, '', line) # Get rid of punctuation"

    def generate_stopwords(self, dataset):
        unigram_dict = {}
        stop_words = set(stopwords.words('english'))

        with open(dataset, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    row = self.clean_line(row[0])
                    uni_tokens = nltk.word_tokenize(row)
                    for word in uni_tokens:
                        word = word.lower()
                        if word not in stop_words:
                            freq = unigram_dict.get(word)
                            if freq:
                                unigram_dict[word] += 1
                            else:
                                unigram_dict[word] = 1
                    line_count += 1
            print(str(line_count) + " lines read.")
        uni_sorted = dict(sorted(unigram_dict.items(), key=lambda item: item[1], reverse=True))
        keys = list(uni_sorted.keys())
        new_stop_words = list(uni_sorted.keys())[0:int(len(keys)/1000)] # add top .1% to the stopwords list
        stop_words.update(set(new_stop_words))
        return stop_words

    def generate_index(self, stop_words, dataset):
        ps = PorterStemmer()
        index = {}
        doc_index = {}

        with open(dataset, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    doc = Document(row[1], row[0], line_count-1)
                    row = self.clean_line(row[0])
                    tokens = nltk.word_tokenize(row)
                    for word in tokens:
                        word = word.lower()
                        if word not in stop_words:
                            doc.word_count += 1
                            word = ps.stem(word)
                            if index.get(word):
                                if index[word].get(line_count-1):
                                    # Word has been seen before in this document
                                    index[word][line_count-1] +=1
                                else:
                                    # Word has been seen before, but not in this document
                                    index[word][line_count-1] = 1
                            else:
                                # Word has not been seen before
                                index[word] = {}
                                index[word][line_count-1] = 1
                    line_count += 1
                    doc_index[doc.id] = doc
            with open(constant.DOC_PATH, 'wb') as outp:
                pickle.dump(doc_index, outp, -1)
            print(str(line_count) + " lines read.")
        return index