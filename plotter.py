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

def loadModel(styleName):
	styleName = styleName
	lineLenDist = pickle.load(open("lineLenDist" + styleName + ".p", "rb"))
	gramDict = pickle.load(open("gramDict" + styleName + ".p", "rb"))
	rhymeDist = pickle.load(open("rhymeDist" + styleName + ".p", "rb"))
	rhymingDictionary = pickle.load(open("rhymingDictionary" + styleName + ".p", "rb"))

def lineLenDistGraph():
	### Generate Line Length Distribution graph
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


def rhymeDistGraph(rhymePos):
	### Generate Series of Rhyme Distribution Graphs
	plt.figure("Rhymes")

	x = [i for i in range(14)]
	y = [0] * 14

	dist = rhymeDist[rhymePos]
	for pos, prob in dist.iteritems():
		y[pos] = prob

	plt.plot(x, y)
	plt.title(styleName + ": Rhyming Distribution for Pos = {}".format(rhymePos))
	plt.xlabel("Phrase position (syllables)")
	plt.ylabel("Probability of syllable {} rhyming".format(rhymePos))

loadModel('Chance')
lineLenDist()
rhymeDistGraph(14)
plt.show()
