import constants as constant
import pickle
from Tokenize.tokenizer import Tokenizer

tokenizer = Tokenizer(constant.FILEPATH)
stop_words = tokenizer.generate_stopwords()
with open('stop_words.pkl', 'wb') as outp:
    pickle.dump(stop_words, outp, -1)

# with open('stop_words.pkl', 'rb') as inp:
#     stop_words = pickle.load(inp)
#     print(stop_words)