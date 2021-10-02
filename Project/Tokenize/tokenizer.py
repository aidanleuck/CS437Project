import nltk
import csv
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

class Tokenizer:

    def __init__(self, dataset):
        self.dataset = dataset

    def generate_stopwords(self):
        unigram_dict = {}
        stop_words = set(stopwords.words('english'))

        with open(self.dataset, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    # Remove the following punctuation: ,."“/)(\[]{}!?:;'$&% and other random punctuation from strange csv file
                    regexPunc = r',|\.|\"|\“|\/|\)|\(|\\|\[|\]|\{|\}|\!|\?|\:|\;|\'|\$|\&|\%'
                    row = re.sub(regexPunc, '', row[0]) # Get rid of punctuation
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
        new_stop_words = list(uni_sorted.keys())[0:int(len(keys)/50)] # add top 2% to the stopwords list
        stop_words.update(set(new_stop_words))
        return stop_words

    def generate_index(self, stop_words):
        ps = PorterStemmer()
        index = {}

        with open(self.dataset, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    regexPunc = r',|\.|\"|\“|\/|\)|\(|\\|\[|\]|\{|\}|\!|\?|\:|\;|\'|\$|\&|\%'
                    row = re.sub(regexPunc, '', row[0]) # Get rid of punctuation
                    tokens = nltk.word_tokenize(row)
                    for word in tokens:
                        word = word.lower()
                        if word not in stop_words:
                            word = ps.stem(word)
                            if index.get(word):
                                index[word].append(line_count-1)
                            else:
                                index[word] = [line_count-1]
                    line_count += 1
            print(str(line_count) + " lines read.")
        return index

        # plt.yscale('log')
        # plt.xscale('log')
        # plt.ylabel("Frequency")
        # plt.xlabel("Word Rank \n\n Top 5 words = " + str(list(uni_sorted.keys())[0:5]))
        # plot1 = plt.figure(1)
        # plt.plot(range(len(unigram_dict)), list(uni_sorted.values()))
        # plt.show()