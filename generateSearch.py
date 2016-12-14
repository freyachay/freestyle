import generation
import searchUtil
import random
import model
import plotter
import constants
from collections import defaultdict


corpus = set()

def dd():
	return defaultdict(float)

def genCorpus(style):
	global corpus
	f = open(style.lower() + "Lyrics.txt")
	contents = f.read()
	corpus = set(model.processPhrase(contents))

# ********* Creating search problem *********

def costFunction(newState):
	(totalPhrase, _ , _) = newState
	phrase = [w.replace("\n", "") for w in totalPhrase] # filter new lines from words
	rhymeDist = generation.rhymeDist

	newWord = phrase[len(phrase)-1]
	newSyllables = model.getSyllables([newWord])
	oldSyllables = model.getSyllables(phrase[:len(phrase)-1])

	cost = 0
	skip = False
	for i in range(len(newSyllables)):
		currSyl = newSyllables[i]
		sylCost = 0
		#print("Cur syl: {}".format(currSyl))
		
		for j in range(len(oldSyllables)):
			found = False
			if skip:  # Polysyllabic rhymes
				skip = False
				continue

			prevSyl = oldSyllables[j]
			for pron in currSyl:
				for targetPron in prevSyl:
					#print("{}, {}".format(pron, targetPron))
					if model.sylRhymes(pron, targetPron):
						found = True

						# Check trailing syllable (if available)
						if (i is not len(newSyllables)-1) and (j is not len(oldSyllables)-1):
							for trailPron in newSyllables[i+1]:
								for trailTargetPron in oldSyllables[j+1]:
									if model.sylRhymes(trailPron, trailTargetPron):
										skip = True
						break
				if found: break
			if not found:
				if i is len(newSyllables) - 1: # Last syllable
					sylCost += ((rhymeDist[i + len(oldSyllables)][j]) * constants.lastSylWeight)
				else:
					sylCost += rhymeDist[i + len(oldSyllables)][j]
		# print("Cost: {}".format(sylCost))
		cost += sylCost
	print(newState)
	print("COST: {}".format(cost))
	return cost

# Takes in a list of words. Returns a list of pruneFluency + pruneRhyming words
# to continue branching on
def pruneFunction(fluentWords, prevTuple):
	print(fluentWords)
	# Fluency
	numFollowing = []
	numRhyming = []
	for word in fluentWords:
		curTuple = prevTuple[1:] + (word,)
		numFollowing.append(len(generation.gramDict[curTuple].keys()))
		numRhyming.append(len(generation.rhymingDictionary[word]))
		topFluent = sorted(range(len(numFollowing)), key=lambda i: numFollowing[i], reverse=True)[:constants.pruneFluency]
		topRhyming = sorted(range(len(numRhyming)), key=lambda i: numRhyming[i], reverse=True)[:constants.pruneRhyming]
	topIndices = list(set(topFluent) | set(topRhyming)) # No duplicates
	return [fluentWords[i] for i in topIndices] # Return a list of words


class PhraseGenProblem(searchUtil.SearchProblem):
    def __init__(self, startGram, lineLens, costFunction, pruneFunction):
        self.startGram = startGram
        self.lineLens = lineLens
        self.costFunction = costFunction
        self.pruneFunction = pruneFunction

    # State = (tuple of words so far in phrase, number of lines so far, target line length)
    def startState(self):
        return (self.startGram, 0, lineLens[0])

    # We have generated enough lines for a complete phrase
    def isEnd(self, state):
        return (state[1] == generation.phraseLen)

    def succAndCost(self, state):
        results = []
        (prevPhrase, prevLineCount, targetLineLen) = state

        # Passing in all fluent next words based on last tuple
        prevTuple = generation.getPrevTuple(prevPhrase)
        prunedWords = self.pruneFunction(generation.gramDict[prevTuple].keys(), prevTuple)
        print(prunedWords)
        print("\n")

        for word in prunedWords:
        	# Ignore words that we don't have pronunciations for
        	if len(model.getSyllables([word])) is 0: 
        		continue

        	succPhrase = prevPhrase + (word,)
        	syllables = model.getSyllables(list(succPhrase))

        	# Add a new line character and get new line length once we've made a line
        	if (len(syllables) >= targetLineLen):
        		word = word + "\n"
        		succPhraseNewline = prevPhrase + (word,)
        		# If done with phrase, indicate with lineLenTarget = -1
        		if (prevLineCount + 1) == generation.phraseLen:
        			newLineLen = -1
        		else:
        			newLineLen = self.lineLens[prevLineCount + 1]
        		newState = (succPhraseNewline, prevLineCount + 1, newLineLen)
        	else:
        		newState = (succPhrase, prevLineCount, targetLineLen)

        	results.append((word, newState, self.costFunction(newState)))

        return results

# ************************************

# Testing

# totalPhrase = ("Butter", "in", "my", "the") # 1 syllable rhyme
# print(costFunction(totalPhrase))
# totalPhrase = ("Butter", "in", "my", "the", "shoe") # no rhyme
# print(costFunction(totalPhrase))
# totalPhrase = ("Butter", "in", "my", "gutter") # 2 syllable rhyme!!
# print(costFunction(totalPhrase))
# totalPhrase = ("Butter", "in", "my", "water") 
# print(costFunction(totalPhrase))


# *********** Solve search problem ******

# Returns a phrase in the form of a list of words
def solve(startGram, lineLens, costFunction):
    ucs = searchUtil.UniformCostSearch(verbose=0)
    ucs.solve(PhraseGenProblem(startGram, lineLens, costFunction, pruneFunction))
    return ucs.actions


# ************************************




# ******* Main ******

for style in constants.styleNames:
	genCorpus(style)
	generation.loadModel(style)

 	totalLyrics = ""
	# Choose a random starting gram
	startGram = random.choice(generation.gramDict.keys())

	# Generate numPhrases phrases
	for i in range(generation.numPhrases):
		# -1 represents when we've generated enough lines
		# lineLens = [generation.sampleLineLength() for i in range(model.phraseLen)]
		lineLen = generation.sampleLineLength()
		# while lineLen > constants.maxLineLen or lineLen is 0:
		# 	lineLen = generation.sampleLineLength()
		lineLens = [8]
		# lineLens.append(-1)
		phrase = solve(startGram, lineLens, costFunction)
		totalLyrics += (' '.join(list(startGram)) + " " + ' '.join(phrase))

		# Get new startGram (last gram in previously generated phrase)
		# startGram = generation.getPrevTuple(phrase[:len(phrase)-1])
		startGram = random.choice(generation.gramDict.keys())

	print(totalLyrics)

	# Evaluation
	distance, fluencyScore = generation.evaluate(style, totalLyrics, False)
	print("Distance: {}".format(distance))
	print("Fluency: {}".format(fluencyScore))
	print("\n")

plotter.plot()

