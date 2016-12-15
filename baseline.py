
import nltk
import random
import collections
import pickle
import constants
import generation
from numpy.random import choice
from nltk.util import ngrams
from collections import Counter
from collections import defaultdict

# Model global variables
styleName = "Hamilton"
gramDict = None
phraseLen = None
n = None

def dd():
	return defaultdict(float)

def loadModel(style):
	global gramDict
	global phraseLen
	global n
	n = constants.n
	phraseLen = constants.phraseLen
	gramDict = pickle.load(open("gramDict" + styleName + "_" + str(phraseLen) + ".p", "rb"))


def generate_word(key):
	if len(gramDict[key]) is 0:
		return ""
	elements = []
	weights = []
	for succ, prob in gramDict[key].iteritems():
		elements.append(succ)
		weights.append(prob)

	return choice(elements, p=weights)


loadModel(styleName)

prevChunk = random.choice(gramDict.keys())
sentence = [prevChunk[i] for i in range(n-1)]

lineCount = 0
currentLength = 0
targetLength = random.randrange(5, 12)
while lineCount < 50:
	nextWord = generate_word(prevChunk)
	while(nextWord is ""):
		nextWord = generate_word(random.choice(gramDict.keys()))
		
	sentence.append(nextWord)
	currentLength += 1
	prevChunk = prevChunk[1:] + (nextWord,)
	if currentLength is targetLength:
		lineCount += 1
		sentence.append("\n")
		targetLength = random.randrange(5, 12)
		currentLength = 0

generatedText = ' '.join(sentence).lower()
print(generatedText)
print("")

distance, fluencyScore = generation.evaluate(styleName, generatedText, False)
print("Distance: {}".format(distance))
print("Fluency: {}".format(fluencyScore))
print("\n")
	
