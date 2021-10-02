import constants as constant
import pickle
from Tokenize.tokenizer import Tokenizer

tokenizer = Tokenizer(constant.FILEPATH)
with open(constant.STOPWORD_PATH, 'rb') as inp:
    stop_words = pickle.load(inp)

index = tokenizer.generate_index(stop_words)
with open(constant.INDEX_PATH, 'wb') as outp:
    pickle.dump(index, outp, -1)