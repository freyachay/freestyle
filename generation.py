import pickle

def dd():
	return defaultdict(float)
	
lineLenDist = pickle.load(open("lineLenDist.p", "rb"))
gramDict = pickle.load(open("gramDict.p", "rb"))
rhymeDict = pickle.load(open("rhymeDist.p", "rb"))

print(lineLenDist)
print(gramDict)
print(rhymeDict)