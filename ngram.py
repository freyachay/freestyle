import nltk
from nltk.util import ngrams

def word_grams(words):
    s = []
    
    for ngram in ngrams(words, 3):
        s.append(' '.join(str(i) for i in ngram))
    return s

print word_grams('one two three four water bottle give me the water'.split(' '))