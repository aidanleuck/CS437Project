import nltk
import csv
import constants
from nltk.stem import PorterStemmer
import re

with open(constants.dataset_name, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
