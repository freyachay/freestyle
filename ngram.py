import nltk
from nltk.util import ngrams
from collections import Counter

def word_grams(words, n):
    gramList = []
    
    for ngram in ngrams(words, n):
        gramList.append(' '.join(str(i) for i in ngram))
    return gramList

bigrams = word_grams('one two three four water bottle give me the water bottle'.split(' '), 2)
print(Counter(bigrams))