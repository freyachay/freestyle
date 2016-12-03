import pickle
import matplotlib.pyplot as plt
from collections import defaultdict


def dd():
	return defaultdict(float)

lineLenDist = pickle.load(open("lineLenDist.p", "rb"))
gramDict = pickle.load(open("gramDict.p", "rb"))
rhymeDist = pickle.load(open("rhymeDist.p", "rb"))
rhymingDictionary = pickle.load(open("rhymingDictionary.p", "rb"))

### Generate Line Length Distribution graph
plt.figure(1)
x = []
y = []
for length, prob in lineLenDist.iteritems():
	x.append(length)
	y.append(prob)
plt.plot(x, y)
plt.title("Chance: Line Length Distribution")
plt.xlabel("Line Length (syllables)")
plt.ylabel("Probability")


### Generate Series of Rhyme Distribution Graphs
plt.figure(2)
rhymePos = 14 # most common line length * number of lines in phrase, i.e. last word in phrase

x = [i for i in range(14)]
y = [0] * 14

dist = rhymeDist[rhymePos]
for pos, prob in dist.iteritems():
	y[pos] = prob

plt.plot(x, y)
plt.title("Chance: Rhyming Distribution for Pos = 14")
plt.xlabel("Phrase position (syllables)")
plt.ylabel("Probability of syllable {} rhyming".format(rhymePos))
plt.show()
