import pickle

# Number of phrases to generate
phraseLen = 2
numPhrases = 10

def dd():
	return defaultdict(float)

lineLenDist = pickle.load(open("lineLenDist.p", "rb"))
gramDict = pickle.load(open("gramDict.p", "rb"))
rhymeDict = pickle.load(open("rhymeDist.p", "rb"))
rhymingDictionary = pickle.load(open("rhymingDictionary.p", "rb"))

print(lineLenDist)
print("\n")
print(gramDict)
print("\n")
print(rhymeDict)
print("\n")
print(rhymingDictionary)

# # Returns a number of syllables for a line
# def sampleLineLength():
# 	return 4
# 	# TO DO

# # ************* Main script ***************

# # Start with a random word
# firstWord = random.choice(gramDict.keys())
# lineLength = sampleLineLength()
# currentPhrase = ""
# currentLineLength = 0

# for _ in range(numPhrases):
# 	for _ in range(phraseLen):
# 		if currentLineLength is lineLength:
# 			currentPhrase += "\n"
# 			currentLineLength = 0