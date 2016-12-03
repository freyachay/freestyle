import pickle
from collections import defaultdict

def dd():
	return defaultdict(float)

styleName = "Nicki"
lineLenDist = pickle.load(open("lineLenDist" + styleName + ".p", "rb"))
gramDict = pickle.load(open("gramDict" + styleName + ".p", "rb"))
rhymeDist = pickle.load(open("rhymeDist" + styleName + ".p", "rb"))
rhymingDictionary = pickle.load(open("rhymingDictionary" + styleName + ".p", "rb"))

print(lineLenDist)

print(sum(lineLenDist.values()))