import nltk
import csv
# import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from modules import Helper
import collections
import numpy as np

dataset_name = 'HW3\docs.csv'
index = {}  # word: [docs]
td_matrix = {}
tt_matrix = {}
ps = PorterStemmer()

help = Helper(set(stopwords.words('english')))


with open(dataset_name, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            document = help.clean_doc(row[0])
            tokens = nltk.word_tokenize(document)
            count = 0
            for word in tokens:
                if help.check_word(word):
                    count +=1
                    word = ps.stem(word)
                    if index.get(word):
                        index[word].append(line_count-1)
                    else:
                        index[word] = [line_count-1]
            line_count += 1
            print(count)
    print(str(line_count) +  " lines read.")

index = collections.OrderedDict(sorted(index.items())) #sort index alphabetically

for term in index: # Create term-document matrix
    td_matrix[term] = []
    for doc in range(line_count-1):
        if doc in index[term]:
            td_matrix[term].append(1)
        else:
            td_matrix[term].append(0)

# Explanation of bitwise AND to find correlation
# action: [1, 0, 0, 0, 0]
# anim  : [1, 0, 1, 1, 0]
#         [1, 0, 0, 0, 0]

for term in td_matrix: # Create term-term matrix
    tt_matrix[term] = {}
    for term_2 in td_matrix:
        val = sum(np.bitwise_and(td_matrix[term], td_matrix[term_2])) # get correlation 
        tt_matrix[term][term_2] = val # Add Correlation to dictionary

# print(tt_matrix)