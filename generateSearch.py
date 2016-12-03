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
class SegmentationProblem(util.SearchProblem):
    def __init__(self, startGram, costFunction):
        self.startGram = startGram
        self.costFunction = costFunction

    # State = (list of words so far in phrase, number of lines so far)
    def startState(self):
        return (list(startGrams), 0)

    # We have generated enough lines for a complete phrase
    def isEnd(self, state):
        return (state[1] == generation.phraseLen)

    def succAndCost(self, state):
    	# List of tuples = (successor state, cost)
        results = []


        return results

# ************************************

# Low fluency + missed rhyme opportunity
def costFunction:
	return 8

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








