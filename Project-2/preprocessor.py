'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""

        lowers = text.lower().strip()

        clear = re.sub(r"[^a-zA-Z0-9 ]", " ", lowers)

        splits = clear.split()
        
        no_stops = []
        for word in splits:
            if word not in self.stop_words:
                no_stops.append(word)
                
        stems = []
        for word in no_stops:
            stems.append(self.ps.stem(word))
            
        # stems = list(set(stems))

        return stems
