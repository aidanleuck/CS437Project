import nltk
import csv
import matplotlib.pyplot as plt

dataset_name = 'sample_dataset.csv'
word_dict = {}

#Process CSV file in dictionary
with open(dataset_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            tokens = nltk.word_tokenize(row[0])
            # tokens = list(nltk.bigrams(row[0].split()))
            for word in tokens:
                word = word.lower()
                freq = word_dict.get(word)
                if freq:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
            line_count += 1
    print(word_dict)
    # print(str(line_count) +  " lines read.")

words_sorted = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True))
plt.yscale('log')
plt.xscale('log')
plt.plot(range(len(word_dict)), list(words_sorted.values()))
plt.show()
