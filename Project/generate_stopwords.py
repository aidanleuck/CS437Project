import constants as constant
import pickle
from Tokenize.tokenizer import Tokenizer
from codetiming import Timer

t = Timer(name="class")
t.start()
tokenizer = Tokenizer(constant.FILEPATH)
print("generate stopwords")
stop_words = tokenizer.generate_stopwords()
print("writing to file")
with open(constant.STOPWORD_PATH, 'wb') as outp:
    pickle.dump(stop_words, outp, -1)
t.stop()