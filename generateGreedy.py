import generation
import plotter
import model
import random
import constants
from numpy.random import choice
from collections import defaultdict

numPhrases = constants.numPhrases
phraseLen = constants.phraseLen


def dd():
	return defaultdict(float)

# Given a probability distribution, returns a list of samples, one per peak
# Peaks are demarkated by local minima
def samplePeaks(distribution, rhymePos):
	minIndices = []
	items = distribution.keys()

	for i in range(len(items)):
		if i is 0: continue # First element
		if i is len(items) - 1: continue # Last element

		prev = distribution[items[i-1]]
		curr = distribution[items[i]]
		next = distribution[items[i+1]]

		if curr < prev and curr < next:
			minIndices.append(i)

	peakChoices = []
	for i in range(len(minIndices) - 1):
		left = minIndices[i]
		right = minIndices[i+1]
		subDist = defaultdict(float)

		# Transfer distribution values in range
		totalSum = 0
		for index in range(left + 1, right): # Excludes minima themselves
			subDist[index] = distribution[index]
			totalSum += distribution[index]

		# Normalize
		weights = []
		for k, v in subDist.iteritems():
			subDist[k] = v/totalSum
			weights.append(subDist[k])

		# Given chunk of distribution, sample from it
		sample = choice(subDist.keys(), p=weights)
		if sample not in rhymePos:
			peakChoices.append(sample)
	return peakChoices


# Generates text given loaded model
# Returns a string of generated text
def generate():
	lineLenDist = generation.lineLenDist
	gramDict = generation.gramDict
	rhymeDist = generation.rhymeDist
	rhymingDictionary = generation.rhymingDictionary

	# Start with a random word
	firstGram = random.choice(gramDict.keys())

	currentPhrase = [word for word in firstGram]
	totalPhrase = [word for word in firstGram]

	currentPhraseLength = len(model.getSyllables(currentPhrase))
	currentLineLength = len(model.getSyllables(currentPhrase))
	totalPhraseLength = len(model.getSyllables(currentPhrase))

	for _ in range(numPhrases):
		lineLengths = [generation.sampleLineLength() for i in range(phraseLen)]

		# Pick rhyming positions for phrase
		totalLen = sum(lineLengths)
		# Add ends of lines
		rhymePos = [lineLengths[0] - 1]
		for i in range(1, len(lineLengths)):
			rhymePos.append(rhymePos[i-1] + lineLengths[i])

		# Sample additional rhymes (one sample per peak)
		phraseRhymeDist = rhymeDist[totalLen] # Dictionary
		rhymePos += samplePeaks(phraseRhymeDist, rhymePos)
		rhymePos = sorted(rhymePos)

		for targetLineLength in lineLengths:
			# Generate line
			while (currentLineLength < targetLineLength):
				# See if we need to rhyme
				nextWord = ""
				if (currentPhraseLength in rhymePos):
					print("Rhyme needed at pos {}".format(currentPhraseLength))
					nextWord = generation.getRhymingWord(currentPhrase, currentPhraseLength, rhymePos) 
					print("Found? : {}".format(nextWord))
				# Either we don't need to rhyme or we couldn't find a rhyme
				if (nextWord is ""):
					# Generate word from n grams
					nextWord = generation.generateWord(generation.getPrevTuple(totalPhrase))
					while(nextWord is ""):
						nextWord = generation.generateWord(random.choice(gramDict.keys()))

				currentPhrase.append(nextWord)
				totalPhrase.append(nextWord)
				currentLineLength += len(model.getSyllables([nextWord]))

				# print("Curr line length = {}".format(currentLineLength))
				# print("Next word: {}".format(nextWord))
				# print("\n")

				currentPhraseLength += len(model.getSyllables([nextWord]))
				totalPhraseLength += len(model.getSyllables([nextWord]))
			currentPhrase.append("\n")
			totalPhrase.append("\n")
			currentLineLength = 0
		currentPhraseLength = 0
		currentPhrase = []

	return ' '.join(totalPhrase)

# ******* Main **********

for style in constants.styleNames:
	generation.loadModel(style)
	generatedText = generate()
	print(generatedText)
	rhymeScore, fluencyScore = generation.evaluate(style, generatedText, False)
	print("Rhyme score: {}".format(rhymeScore))
	print("Fluency: {}".format(fluencyScore))
	print("\n")
plotter.plot()







