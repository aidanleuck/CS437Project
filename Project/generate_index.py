import constants as constant
from Tokenize.tokenizer import Tokenizer

tokenizer = Tokenizer(constant.FILEPATH)
print(str(tokenizer.generate_stopwords()))