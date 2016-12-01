import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

sentence = "Happily I am sitting, at a table with! a water bottle \n Merrily we go"

tokens = wordpunct_tokenize(sentence)
print(tokens)
punct = ['.', ',', '!', ':', ';']

filtered = [word for word in tokens if word not in punct]

print(filtered)
