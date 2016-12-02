import pickle
import random
import model
from collections import defaultdict

# Number of phrases to generate
n = model.n
phraseLen = model.phraseLen
numPhrases = 10

def dd():
	return defaultdict(float)

lineLenDist = pickle.load(open("lineLenDist.p", "rb"))
gramDict = pickle.load(open("gramDict.p", "rb"))
rhymeDist = pickle.load(open("rhymeDist.p", "rb"))
rhymingDictionary = pickle.load(open("rhymingDictionary.p", "rb"))

# Uses ngram dict to generate next word
def generateWord(prev):
	if len(gramDict[prev]) is 0:
		print("generate returning empty")
		return ""
	return random.choice(gramDict[prev])


# Returns a number of syllables for a line
def sampleLineLength():
	return 16
	# TO DO

def getRhymeTarget(pos):
	distribution = rhymeDist[pos]


def getPrevTuple(currentPhrase, pos):
	prevGram = tuple(currentPhrase[(len(currentPhrase) - n + 1):])
	if prevGram[len(prevGram) - 1] is "\n":
		return tuple(currentPhrase[(len(currentPhrase) - n): len(currentPhrase) - 1])
	return prevGram

# Takes in a list of pronunciations of a syllable.
# Returns a word that starts by rhyming with given syllable, or returns "" if nothing found
def findRhyme(sylProns):
	# Get stressed vowel + suffix from syl
	print(sylProns)

	# Try all pronunciations of syl
	for pron in sylProns:
		stressed = [s for s in pron if model.containsDigit(s)][0]
		print(stressed)
		stressIndex = pron.index(stressed)
		suffix = pron[stressIndex + 1:]
		key = stressed + ''.join(suffix)

		print(key)
		# Look rhyming sound up in rhyming dictionary, find a word!
		rhymingWords = rhymingDictionary[key]
		print(rhymingWords)
		if len(rhymingWords) > 0:
			# **** Returns random word that rhymes
			return random.sample(rhymingWords, 1)[0]

	# No rhymes found for any pronunciation
	return ""

def sampleRhymeDist(currentPhrase, pos):
	# Sorted rhyme targets sorted by probability
	targets = rhymeDist[pos]
	sortedTargets = sorted(targets, key=targets.get, reverse = True)
	phraseSyllables = model.getSyllables(currentPhrase)
	for target in sortedTargets:
		rhymeWord = findRhyme(phraseSyllables[target])
		if rhymeWord is not "":
			return rhymeWord
	return ""

# ************* Main script ***************

# Start with a random word
firstGram = random.choice(gramDict.keys())
lineLength = sampleLineLength()
currentPhrase = [word for word in firstGram]
currentLineLength = len(model.getSyllables(currentPhrase))


print(lineLength)
for _ in range(numPhrases):
	for _ in range(phraseLen):
		# Generate line
		while (currentLineLength < lineLength):
			# Does the next word need to rhyme?
			rhymeTarget = getRhymeTarget(currentLineLength)
			if (rhymeTarget is not -1): # We need a rhyme!
				print("We need a rhyme!")
				nextWord = sampleRhymeDist(currentPhrase, currentLineLength)

			# Either we don't need to rhyme or we couldn't find a rhyme
			if (nextWord is "" or rhymeTarget is -1):
				print("Couldn't find one or don't need one")
				# Generate word from n grams
				nextWord = generateWord(getPrevTuple(currentPhrase, currentLineLength))
				while(nextWord is ""):
					nextWord = generateWord(random.choice(gramDict.keys()))

			print("THE NEXT WORD IS: {}".format(nextWord))
			currentPhrase.append(nextWord)
			currentLineLength += len(model.getSyllables(nextWord))
		currentPhrase.append("\n")
		currentLineLength = 0


print(' '.join(currentPhrase))
		