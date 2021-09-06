import nltk
import csv
import matplotlib.pyplot as plt

dataset_name = 'sample_dataset.csv'
ratio_dict = {}
unigram_dict = {}

with open(dataset_name, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    words_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            uni_tokens = nltk.word_tokenize(row[0].lower())
            bi_tokens = list(nltk.bigrams(row[0].lower().split()))
            for word in uni_tokens:
                words_count += 1
                freq = unigram_dict.get(word)
                if freq:
                    unigram_dict[word] += 1
                else:
                    unigram_dict[word] = 1
                ratio_dict[words_count] = len(unigram_dict)
    print(str(line_count) +  " lines read.")

plt.plot(range(len(ratio_dict)), list(ratio_dict.values()))
plt.ylabel("Words in Vocabulary")
plt.xlabel("Words in Collection\n\n Vocab size: " + str(len(unigram_dict)) + "\nTotal words in corpus: " + str(words_count))
plt.show()