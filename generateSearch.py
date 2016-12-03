import generation
import searchUtil
import model

corpus = set()

def genCorpus(style):
	global corpus
	f = open(style.lower() + "Lyrics.txt")
	contents = f.read()
	corpus = set(model.processPhrase(contents))

# ********* Creating search problem *********

# Low fluency (eh) + missed rhyme opportunity (WORSE)
def costFunction(newState):

	 

class SegmentationProblem(util.SearchProblem):
    def __init__(self, startGram, costFunction):
        self.startGram = startGram
        self.costFunction = costFunction

    # State = (list of words so far in phrase, number of lines so far, target line length)
    def startState(self):
        return (list(startGrams), 0, generation.sampleLineLength())

    # We have generated enough lines for a complete phrase
    def isEnd(self, state):
        return (state[1] == generation.phraseLen)

    def succAndCost(self, state):
    	# List of tuples = (successor state, cost)
        results = []
        (prevPhrase, prevLines, targetLineLen) = state

        for word in corpus:
        	succPhrase = prevPhrase.append(word)
        	syllables = model.getSyllables(succPhrase)

        	# Add a new line character and get new line length once we've made a line
        	if (syllables >= targetLineLen):
        		succPhrase.append("\n")
        		newState = (succPhrase, prevLines + 1, generation.sampleLineLength())
        	else:
        		newState = (succPhrase, prevLines, targetLineLen)

        	results.append(newState, costFunction(newState))

        return results

# ************************************

# *********** Solve search problem ******

def solve(startGram, unigramCost):
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(startGram, costFunction))
    return ' '.join(ucs.actions)


# ************************************

# ******* Main ******

for style in ["Chance", "Nicki"]:
	genCorpus(style)
	print(corpus)

	# Run solve numPhrases times








