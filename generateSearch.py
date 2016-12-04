import generation
import searchUtil
import random
import model
import plotter
from collections import defaultdict

corpus = set()

# For cost function
fluencyWeight = 1
rhymeWeight = 10

def dd():
	return defaultdict(float)

def genCorpus(style):
	global corpus
	f = open(style.lower() + "Lyrics.txt")
	contents = f.read()
	corpus = set(model.processPhrase(contents))

# ********* Creating search problem *********

# Low fluency (eh) + missed rhyme opportunity (WORSE)
def costFunction(newState):
	(totalPhrase, lineCount, targetLineLen) = newState
	phrase = [w.replace("\n", "") for w in totalPhrase] # filter new lines from words
	rhymeDist = generation.rhymeDist
	phraseSyllables = model.getSyllables(phrase)

	newWord = phrase[len(phrase)-1]
	newSyllables = model.getSyllables([newWord])

	# Determines cost of each syllable of new word, end to front
	cost = 0
	for i in range(len(newSyllables)):
		syllable = newSyllables[i]
		positionDist = rhymeDist[len(phraseSyllables) - 1 - i]

		for pos, prob in positionDist.iteritems():
			found = False
			if prob < generation.rhymeThresh: continue

			# We're supposed to rhyme! Did we?
			targetSyl = phraseSyllables[pos]

			for pron in syllable:
				for targetPron in targetSyl:
					if model.sylRhymes(pron, targetPron):
						found = True
						break
				if found: break

			# Cost is proportional to how much you were supposed to rhyme
			if not found:
				cost += (prob * rhymeWeight)

	# prevGram is the gram before the word we just added
	# prevGram = generation.getPrevTuple(phrase[:len(phrase)-1])
	# fluentSuccessors = generation.gramDict[prevGram]

	# if newWord not in fluentSuccessors:
	# 	cost += fluencyWeight
	return cost
	 

class PhraseGenProblem(searchUtil.SearchProblem):
    def __init__(self, startGram, lineLens, costFunction):
        self.startGram = startGram
        self.lineLens = lineLens
        self.costFunction = costFunction

    # State = (tuple of words so far in phrase, number of lines so far, target line length)
    def startState(self):
        return (startGram, 0, generation.sampleLineLength())

    # We have generated enough lines for a complete phrase
    def isEnd(self, state):
        return (state[1] == generation.phraseLen)

    def succAndCost(self, state):
    	print(state)
        results = []
        (prevPhrase, prevLineCount, targetLineLen) = state

        # Iterate through fluent words
        for word in generation.gramDict[generation.getPrevTuple(prevPhrase)]:
        	# Ignore words that we don't have pronunciations for
        	if len(model.getSyllables([word])) is 0: 
        		print("Don't have pronunciation")
        		continue

        	succPhrase = prevPhrase + (word,)
        	syllables = model.getSyllables(list(succPhrase))

        	# Add a new line character and get new line length once we've made a line
        	if (len(syllables) >= targetLineLen):
        		word = word + "\n"
        		newState = (succPhrase, prevLineCount + 1, lineLens[prevLineCount + 1])
        	else:
        		newState = (succPhrase, prevLineCount, targetLineLen)

        	results.append((word, newState, costFunction(newState)))
        print(results)
        print("\n")
        return results

# ************************************

# *********** Solve search problem ******

# Returns a phrase in the form of a list of words
def solve(startGram, costFunction):
    ucs = searchUtil.UniformCostSearch(verbose=0)
    ucs.solve(PhraseGenProblem(startGram, costFunction))
    return ucs.actions


# ************************************

# ******* Main ******

for style in ["Chance"]:
	genCorpus(style)
	generation.loadModel(style)

 	totalLyrics = []
	# Choose a random starting gram
	startGram = random.choice(generation.gramDict.keys())

	# Generate numPhrases phrases
	for i in range(generation.numPhrases):
		# -1 represents when we've generated enough lines
		lineLens = [generation.sampleLineLength() for i in range(phraseLen)].append(-1)
		phrase = solve(startGram, lineLens, costFunction)
		totalLyrics += phrase

		# Get new startGram (last gram in previously generated phrase)
		startGram = generation.getPrevTuple(phrase[:len(phrase)-1])

	# Convert final state tuple to list
	print(' '.join(totalLyrics))

	# Evaluation
	distance = generation.evaluate(style, ' '.join(totalLyrics))
	print(distance)
	print("\n")

plotter.plot()

