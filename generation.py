import pickle
import random
import model
import plotter
import constants
from numpy.random import choice
from collections import defaultdict
from collections import Counter

# Model global variables
lineLenDist = None
gramDict = None
rhymeDist = None
rhymingDictionary = None

# Number of phrases to generate
n = constants.n
phraseLen = constants.phraseLen
numPhrases = constants.numPhrases

def dd():
	return defaultdict(float)

def loadModel(styleName):
	global lineLenDist 
	global gramDict
	global rhymeDist 
	global rhymingDictionary
	lineLenDist = pickle.load(open("lineLenDist" + styleName + "_" + str(phraseLen) + ".p", "rb"))
	gramDict = pickle.load(open("gramDict" + styleName + "_" + str(phraseLen) + ".p", "rb"))
	rhymeDist = pickle.load(open("rhymeDist" + styleName + "_" + str(phraseLen) + ".p", "rb"))
	rhymingDictionary = pickle.load(open("rhymingDictionary" + styleName + "_" + str(phraseLen) + ".p", "rb"))

# Uses ngram dict to generate next word
def generateWord(prev):
	if len(gramDict[prev].keys()) is 0: return ""

	elements = []
	weights = []

	for k, v in gramDict[prev].iteritems():
		elements.append(k)
		weights.append(v)

	return choice(elements, p=weights)

# Returns a number of syllables for a line
def sampleLineLength():
	elements = []
	weights = []

	for k, v in lineLenDist.iteritems():
		elements.append(k)
		weights.append(v)

	return choice(elements, p=weights)

# Returns the last tuple in a phrase
def getPrevTuple(phrase):
	prevGram = tuple(phrase[(len(phrase) - n + 1):])
	if prevGram[len(prevGram) - 1] is "\n":
		return tuple(phrase[(len(phrase) - n): len(phrase) - 1])
	return prevGram

# Takes in a list of pronunciations of a syllable.
# Returns a word that starts by rhyming with given syllable, or returns "" if nothing found
def findRhyme(sylProns):
	# Get stressed vowel + suffix from syl

	# Try all pronunciations of syl
	for pron in sylProns:
		stressed = [s for s in pron if model.minusDigit(s) in model.vowelPhenomes][0]
		stressIndex = pron.index(stressed)
		suffix = pron[stressIndex + 1:]
		key = stressed + ''.join(suffix)

		# Look rhyming sound up in rhyming dictionary, find a word!
		rhymingWords = rhymingDictionary[key]

		if len(rhymingWords) is not 0:
			return random.sample(rhymingWords, 1)[0]

	# No rhymes found for any pronunciation
	return ""

# Takes in a current position to be filled, 
# looks for a word that rhymes with one of the rhyme targets specified by 
# position in rhymePos (rhymePos expected to be sorted)
def getRhymingWord(currentPhrase, pos, rhymePos):
	phraseSyllables = model.getSyllables(currentPhrase)
	for i in range(rhymePos.index(pos)):
		targetPos = rhymePos[i]
		rhymeWord = findRhyme(phraseSyllables[targetPos])
		if rhymeWord is not "":
			return rhymeWord
	return ""

# Takes in a generatedText, generates a model based on the generated text,
# and returns the distance squared between the rhyme distribution of the 
# generated model and target model 
def evaluate(targetStyle, generatedText, plot):
	loadModel(targetStyle)
	# Create genModel: i.e. the model of our generated text
	(genRhymeDist, _, _, _) = model.buildModel(generatedText)

	numRhymes = 0

	lines = generatedText.splitlines()
	numPhrases = len(lines)/phraseLen
	print(numPhrases)
	for i in range(numPhrases): # For each phrase
		phrase = [lines[j] for j in range(2*i, (2*i) + phraseLen)]

		phraseWords = []
		for line in phrase:
			for word in line.split():
				phraseWords.append(word)

		
		phraseSyls = model.getSyllables(phraseWords)
		for x in range(len(phraseSyls)):
			for y in range(x):
				found = False
				syl1 = phraseSyls[x]
				syl2 = phraseSyls[y]

				def existsRhymeCombo(syl1, syl2):
					for pron1 in syl1:
						for pron2 in syl2:
							if model.sylRhymes(pron1, pron2): return True
					return False

				if existsRhymeCombo(syl1, syl2):
					xTemp = x
					yTemp = y
					consecCount = 0
					consecDict = defaultdict(int)
					while existsRhymeCombo(phraseSyls[xTemp], phraseSyls[yTemp]):
						consecCount += 1
						numRhymes += 1
						xTemp += 1
						yTemp += 1
						if xTemp > len(phraseSyls)-1 or yTemp > x: break
					value = consecDict[consecCount]
					consecDict[consecCount] = value + 1

	rhymeScore = float(numRhymes)/numPhrases

	# numSamples = 2
	if plot:
		for i in range(5, 20):
			lineLen = sampleLineLength()
			# Plot graph of generated rhyme dist and model rhyme dist at pos
			plotter.evaluationGraph(targetStyle, genRhymeDist, lineLen)

	# Evaluate fluency
	fluencyScore = 0

	for gram in model.generateGrams(generatedText.split()):
		key = tuple(gram.split()[:n-1])
		successor = gram.split()[n-1]
		fluencyScore += gramDict[key][successor]

	return (rhymeScore, fluencyScore/len(generatedText.split()))








		