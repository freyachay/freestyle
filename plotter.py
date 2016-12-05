import pickle
import matplotlib.pyplot as plt
from collections import defaultdict


# Model global variables
lineLenDist = None
gramDict = None
rhymeDist = None 
rhymingDictionary = None
styleName = None

def dd():
	return defaultdict(float)

def loadModel(style):
	global lineLenDist 
	global gramDict
	global rhymeDist 
	global rhymingDictionary
	global styleName
	styleName = style
	lineLenDist = pickle.load(open("lineLenDist" + styleName + "_4.p", "rb"))
	gramDict = pickle.load(open("gramDict" + styleName + "_4.p", "rb"))
	rhymeDist = pickle.load(open("rhymeDist" + styleName + "_4.p", "rb"))
	rhymingDictionary = pickle.load(open("rhymingDictionary" + styleName + "_4.p", "rb"))

# Generate Line Length Distribution graph
def lineLenDistGraph(style):
	loadModel(style)
	lineLenDist[0] = 0	
	plt.figure("Lines")
	x = []
	y = []
	for length, prob in lineLenDist.iteritems():
		x.append(length)
		y.append(prob)
	plt.plot(x, y)
	plt.title(styleName + ": Line Length Distribution")
	plt.xlabel("Line Length (syllables)")
	plt.ylabel("Probability")

# Generate of Rhyme Distribution Graph for rhymePos
def rhymeDistGraph(distribution, rhymePos):
	plt.figure("Rhymes: {}".format(rhymePos))

	x = [i for i in range(rhymePos)]
	y = [0] * rhymePos

	for pos, prob in distribution[rhymePos].iteritems():
		y[pos] = prob

	plt.plot(x, y)
	plt.title(styleName + ": Rhyming Distribution for Pos = {}".format(rhymePos))
	plt.xlabel("Phrase position (syllables)")
	plt.ylabel("Probability of syllable {} rhyming".format(rhymePos))

def evaluationGraph(targetStyle, genRhymeDist, rhymePos):
	loadModel(targetStyle)
	rhymeDistGraph(rhymeDist, rhymePos)
	rhymeDistGraph(genRhymeDist, rhymePos)
	

def plot():
	plt.show()

# loadModel('Nicki')
# lineLenDistGraph('Nicki')
# rhymeDistGraph(rhymeDist, 14)
# plot()
