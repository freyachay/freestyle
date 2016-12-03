import generation
import plotter
import model
import random
from collections import defaultdict

# # Model global variables
# lineLenDist = None
# gramDict = None
# rhymeDist = None
# rhymingDictionary = None

def dd():
	return defaultdict(float)

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

	for _ in range(generation.numPhrases):
		for _ in range(generation.phraseLen):
			targetLineLength = generation.sampleLineLength()
			# Generate line
			while (currentLineLength < targetLineLength):
				# See if we need to rhyme
				nextWord = generation.sampleRhymeDist(currentPhrase, currentLineLength)

				# Either we don't need to rhyme or we couldn't find a rhyme
				if (nextWord is ""):
					# Generate word from n grams
					nextWord = generation.generateWord(generation.getPrevTuple(totalPhrase, totalPhraseLength))
					while(nextWord is ""):
						nextWord = generation.generateWord(random.choice(gramDict.keys()))

				currentPhrase.append(nextWord)
				totalPhrase.append(nextWord)
				currentLineLength += len(model.getSyllables([nextWord]))
				currentPhraseLength += len(model.getSyllables([nextWord]))
				totalPhraseLength += len(model.getSyllables([nextWord]))
			currentPhrase.append("\n")
			totalPhrase.append("\n")
			currentLineLength = 0
		currentPhraseLength = 0
		currentPhrase = []

	return ' '.join(totalPhrase)

generation.loadModel("Chance")
generatedText = generate()
print(generatedText)
distance = generation.evaluate("Chance", generatedText)
print(distance)
plotter.plot()