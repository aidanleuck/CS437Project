import constants as constant
import pickle
from Tokenize.tokenizer import Tokenizer

tokenizer = Tokenizer(constant.FILEPATH)
stop_words = tokenizer.generate_stopwords()
with open(constant.STOPWORD_PATH, 'wb') as outp:
    pickle.dump(stop_words, outp, -1)