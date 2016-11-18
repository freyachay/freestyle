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

		gramDict[key].append(words[n-1])
	return gramDict

def generate_word(key, gramDict, words):
	if len(gramDict[key]) is 0:
		return ""
		#return random.choice(words)
	return random.choice(gramDict[key])

n = 2
f = open('chanceLyrics.txt')
contents = f.read()

grams = generate_grams(contents.split(' '), n)
freqTable = Counter(grams)

gramDict = create_dict(grams, n)

prevChunk = random.choice(gramDict.keys())
sentence = [prevChunk[i] for i in range(n-1)]

currentLength = 0
targetLength = random.randrange(5, 12)
for i in range(100):
	nextWord = generate_word(prevChunk, gramDict, contents.split())
	while(nextWord is ""):
		nextWord = generate_word(random.choice(gramDict.keys()), gramDict, contents.split())
	
	sentence.append(nextWord)
	currentLength += 1
	prevChunk = prevChunk[1:] + (nextWord,)
	if currentLength is targetLength:
		sentence.append("\n")
		targetLength = random.randrange(5, 12)
		currentLength = 0
print(' '.join(sentence).lower())
	
	
