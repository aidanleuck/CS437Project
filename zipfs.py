import nltk
import csv
import matplotlib.pyplot as plt

dataset_name = 'IMDB Dataset.csv'
unigram_dict = {}
bigram_dict = {}

def to_lower_case(s):
    for item in range(len(s)):
        s[item] = str(s[item]).lower()
    return s

# Process CSV file in dictionary
with open(dataset_name, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            uni_tokens = nltk.word_tokenize(row[0].lower())
            bi_tokens = list(nltk.bigrams(row[0].lower().split()))
            for word in uni_tokens:
                freq = unigram_dict.get(word)
                if freq:
                    unigram_dict[word] += 1
                else:
                    unigram_dict[word] = 1
            for tup in bi_tokens:
                freq = bigram_dict.get(tup)
                if freq:
                    bigram_dict[tup] += 1
                else:
                    bigram_dict[tup] = 1
            line_count += 1
    print(str(line_count) +  " lines read.")

uni_sorted = dict(sorted(unigram_dict.items(), key=lambda item: item[1], reverse=True))
bi_sorted = dict(sorted(bigram_dict.items(), key=lambda item: item[1], reverse=True))
plt.yscale('log')
plt.xscale('log')
plt.ylabel("Frequency")
plt.xlabel("Word Rank \n\n Top 5 words = " + str(list(uni_sorted.keys())[0:5]))
plot1 = plt.figure(1)
plt.plot(range(len(unigram_dict)), list(uni_sorted.values()))
plot2 = plt.figure(2)
plt.yscale('log')
plt.xscale('log')
plt.ylabel("Frequency")
plt.xlabel("Bigram Rank \n\n Top 5 bigrams = " + str(list(bi_sorted.keys())[0:5]))
plt.plot(range(len(bigram_dict)), list(bi_sorted.values()))
plt.show()