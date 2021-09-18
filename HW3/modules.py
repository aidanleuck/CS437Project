import re

class Helper:

    def __init__(self, stop_words):
        self.stop_words = stop_words

    def remove_punctuation(self, document, regexPunc=r',|\.|\"|\/|\)|\(|\:'):
        document = re.sub(regexPunc, '', document)
        return document

    def remove_HTML(self, document, regexHTML=r'<br\s?>'):
        document = re.sub(regexHTML, '', document)
        return document

    def clean_doc(self, document):
        return self.remove_HTML(self.remove_punctuation(document)).lower()

    def check_word(self, s):
        if s.lower() in self.stop_words:
            return False
        return True