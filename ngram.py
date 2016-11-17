import nltk
import random
import collections
from nltk.util import ngrams
from collections import Counter

def generate_grams(words, n):
    gramList = []
    
    for ngram in ngrams(words, n):
        gramList.append(' '.join(str(i) for i in ngram))
    return gramList

def create_dict(grams, n):
	gramDict = collections.defaultdict(list)
	for gram in grams:
		words = gram.split()

		key = ()
		for i in range(n-1):
			key = key + (words[i],)

		print(key)
		gramDict[key].append(words[n-1])
		print(words[n-1])
	return gramDict

def generate_word(key, gramDict):
	return random.choice(gramDict[key])

n = 3
grams = generate_grams('one two three four the water bottle give me the water bottle'.split(' '), n)
freqTable = Counter(grams)
print(freqTable)

gramDict = create_dict(grams, n)
print(gramDict)

prevChunk = random.choice(gramDict.keys())
sentence = [prevChunk[i] for i in range(n-1)]

for i in range(5):
	nextWord = generate_word(prevChunk, gramDict)
	sentence.append(nextWord)
	prevChunk = prevChunk[1:] + (nextWord,)
print(' '.join(sentence))
	
	
