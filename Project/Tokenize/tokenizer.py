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
                    # Remove the following punctuation: ,."“/)(\[]{}!?:;'$&% and other random punctuation from strange csv file
                    regexPunc = r',|\.|\"|\“|\/|\)|\(|\\|\[|\]|\{|\}|\!|\?|\:|\;|\'|\$|\&|\%|™|œ|Â|(âˆ’)|(Ä±)|(ÅŸ)'
                    row = re.sub(regexPunc, '', row[0]) # Get rid of punctuation
                    row = re.sub(r'-|(â€)|(âˆ’)', ' ', row) # Replace hyphens with spaces
                    row = re.sub(r'(Ã¨)|(Ã©)', 'e', row) # Replace e's with accents with e's
                    row = re.sub(r'(Ã¸)', 'o', row) # Replace special character o's with o's
                    row = re.sub(r'(Ã¤)|(Ã¡)', 'a', row) # Replace a's with accents with a's
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
        new_stop_words = list(uni_sorted.keys())[0:int(len(keys)/20)] # add top 5% to the stopwords list
        stop_words.update(set(new_stop_words))
        plt.yscale('log')
        plt.xscale('log')
        plt.ylabel("Frequency")
        plt.xlabel("Word Rank \n\n Top 5 words = " + str(list(uni_sorted.keys())[0:5]))
        plot1 = plt.figure(1)
        plt.plot(range(len(unigram_dict)), list(uni_sorted.values()))
        plt.show()
        return stop_words

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
        #                               ø -> Ã¸
        # Went up to line 58, all seem to have some kind of special character a infront of it.