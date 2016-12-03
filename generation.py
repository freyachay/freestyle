import pickle
import random
import model
import plotter
from numpy.random import choice
from collections import defaultdict

# Model global variables
lineLenDist = None
gramDict = None
rhymeDist = None
rhymingDictionary = None

# Number of phrases to generate
n = model.n
phraseLen = model.phraseLen
numPhrases = 1
rhymeThresh = 0.01

def dd():
	return defaultdict(float)

def loadModel(styleName):
	global lineLenDist 
	global gramDict
	global rhymeDist 
	global rhymingDictionary
	lineLenDist = pickle.load(open("lineLenDist" + styleName + ".p", "rb"))
	gramDict = pickle.load(open("gramDict" + styleName + ".p", "rb"))
	rhymeDist = pickle.load(open("rhymeDist" + styleName + ".p", "rb"))
	rhymingDictionary = pickle.load(open("rhymingDictionary" + styleName + ".p", "rb"))

# Uses ngram dict to generate next word
def generateWord(prev):
	if len(gramDict[prev]) is 0:
		return ""
	return random.choice(gramDict[prev])


# Returns a number of syllables for a line
def sampleLineLength():
	elements = []
	weights = []

	for k, v in lineLenDist.iteritems():
		elements.append(k)
		weights.append(v)

	return choice(elements, p=weights)

def getPrevTuple(totalPhrase, pos):
	prevGram = tuple(totalPhrase[(len(totalPhrase) - n + 1):])
	if prevGram[len(prevGram) - 1] is "\n":
		return tuple(totalPhrase[(len(totalPhrase) - n): len(totalPhrase) - 1])
	return prevGram

# Takes in a list of pronunciations of a syllable.
# Returns a word that starts by rhyming with given syllable, or returns "" if nothing found
def findRhyme(sylProns):
	# Get stressed vowel + suffix from syl

	# Try all pronunciations of syl
	for pron in sylProns:
		stressed = [s for s in pron if model.containsDigit(s)][0]
		stressIndex = pron.index(stressed)
		suffix = pron[stressIndex + 1:]
		key = stressed + ''.join(suffix)

		# Look rhyming sound up in rhyming dictionary, find a word!
		rhymingWords = rhymingDictionary[key]
		validRhymingWords = []
		for word in rhymingWords:
			rhymeProns = model.getSyllables(word)[0]
			if rhymeProns is not sylProns: validRhymingWords.append(word)

		if len(rhymingWords) is not 0:
			return random.sample(validRhymingWords, 1)[0]

	# No rhymes found for any pronunciation
	return ""

# Takes in a position, checks rhymeDist, looks for a word that starts with rhyme target (in order of
# rhyme target probability)
def sampleRhymeDist(currentPhrase, pos):
	# Sorted rhyme targets sorted by probability
	targets = rhymeDist[pos]
	if len(targets) is 0: return ""

	# Eliminate targets below probability threshold
	filteredTargets = [i for i in targets.keys() if targets[i] > rhymeThresh]

	sortedTargets = sorted(targets, key=targets.get, reverse = True)
	finalTargets = [t for t in sortedTargets if t in filteredTargets]

	phraseSyllables = model.getSyllables(currentPhrase)
	for target in finalTargets:
		rhymeWord = findRhyme(phraseSyllables[target])
		if rhymeWord is not "":
			return rhymeWord
	return ""

# Takes in a generatedText, generates a model based on the generated text,
# and returns the distance squared between the rhyme distribution of the 
# generated model and target model 
def evaluate(targetStyle, generatedText):
	# Create genModel: i.e. the model of our generated text
	(genRhymeDist, _, _, _) = model.buildModel(generatedText)

	distance = 0
	# Iterate through every postition that appears in model 
	for pos, targetDist in rhymeDist.iteritems():
		genDist = genRhymeDist[pos]
		keySuperSet = set(targetDist.keys()).union(set(genDist.keys()))
		for key in keySuperSet:
			distance += (targetDist[key] - genDist[key])**2

	numSamples = 2
	for i in range(numSamples):
		lineLen = sampleLineLength()
		# Plot graph of generated rhyme dist and model rhyme dist at pos
		plotter.evaluationGraph(targetStyle, genRhymeDist, lineLen)

	return distance
		