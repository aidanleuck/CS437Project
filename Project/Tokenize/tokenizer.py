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
        ps = PorterStemmer()
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
                    # Remove the following punctuation: ,."“/)(\[]{}!?:;'$&
                    regexPunc = r',|\.|\"|\“|\/|\)|\(|\\|\[|\]|\{|\}|\!|\?|\:|\;|\'|\$|\&'
                    row = re.sub(regexPunc, '', row[0])
                    uni_tokens = nltk.word_tokenize(row)
                    for word in uni_tokens:
                        word = word.lower()
                        if word not in stop_words:
                            word = ps.stem(word)
                            freq = unigram_dict.get(word)
                            if freq:
                                unigram_dict[word] += 1
                            else:
                                unigram_dict[word] = 1
                    line_count += 1
            print(str(line_count) + " lines read.")
        uni_sorted = dict(sorted(unigram_dict.items(), key=lambda item: item[1], reverse=True))
        keys = list(uni_sorted.keys())
        plt.yscale('log')
        plt.xscale('log')
        plt.ylabel("Frequency")
        plt.xlabel("Word Rank \n\n Top 5 words = " + str(list(uni_sorted.keys())[0:5]))
        plot1 = plt.figure(1)
        plt.plot(range(len(unigram_dict)), list(uni_sorted.values()))
        top_one_percent = int(len(keys)/100)
        print(top_one_percent)
        return list(uni_sorted.keys())[0:top_one_percent]

        # Weird character replacements: - -> â€
        #                               è -> Ã¨
        #                               ' -> â€™
        #                               - -> â€“
        #                               é -> Ã©
        #                     begin quote -> â€œ
        #                       end quote -> â€
        #                         nothing -> Â
        #                               ä -> Ã¤
        #                               á -> Ã¡
        #                               - -> âˆ’
        #                               ı -> Ä±
        #                               ş -> ÅŸ
        # Went up to line 58, all seem to have some kind of special character a infront of it.