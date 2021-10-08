import constants as constant
import pickle
from Tokenize.tokenizer import Tokenizer
from codetiming import Timer

t = Timer(name="class")
t.start()
tokenizer = Tokenizer(constant.FILEPATH)
print("get stopwords")
with open(constant.STOPWORD_PATH, 'rb') as inp:
    stop_words = pickle.load(inp)

print("generate index")
index = tokenizer.generate_index(stop_words)
print("write to file")
with open(constant.INDEX_PATH, 'wb') as outp:
    pickle.dump(index, outp, -1)

t.stop()