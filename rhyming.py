import nltk
import fmdict
import collections
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

sentence = "Unawareness I am sitting,\n at a table with!\n a water bottle \n Merrily we go"
mainDict = cmudict.dict()
extraDict = fmdict.extraDict

phrase_len = 2

# This takes in a phrase (list of words) and returns a list of syllables made up of sounds.
def getSyllables(phrase):
	syllables = collections.defaultdict(list)
	currentSyl = []

	# For each pronunciation
	globalSylIndex = 0
	localSylIndex = 0
	for word in phrase:
		for pronunciation in mainDict[word.lower()]:
			localSylIndex = globalSylIndex	
			for sound in pronunciation:
				currentSyl.append(sound)

				if (sound[-1]).isdigit():
					prev = syllables[localSylIndex]
					if currentSyl not in prev:
						prev.append(currentSyl)
						syllables[localSylIndex] = prev

					localSylIndex += 1
					currentSyl = []

			if currentSyl is not []:
				lastSyl = syllables[localSylIndex - 1]
				lastPron = lastSyl[-1]
				for sound in currentSyl:
					lastPron.append(sound)

				if lastPron not in lastSyl:
					lastSyl[-1] = lastPron
					syllables[localSylIndex - 1] = lastSyl
				currentSyl = []
				
		globalSylIndex = localSylIndex + 1
	return syllables

print(getSyllables(["graduate", "water", "bottle", "chair"]))

# def getRhymeScore(pron1, pron2):
# 	return 1

# def getPron(word):
# 	# Check fm dict
# 	if word.lower() in extraDict.keys():
# 		return [extraDict[word.lower()]]
# 	# Look in cmudict
# 	if word.lower() in mainDict.keys():
# 		return mainDict[word.lower()]
# 	return None

# def processPhrase(phrase):
# 	tokens = wordpunct_tokenize(sentence)
# 	punct = ['.', ',', '!', ':', ';']
# 	words = [word for word in tokens if word not in punct]

# 	# List of lists of possible pronunciations for each sound in phrase
# 	phraseSounds = []

# 	# For each word in phrase
# 	for word in words:
# 		pron = getPron(word)
# 		if pron is None: continue
# 		for soundIndex in range(len(pron[0])):
# 			soundList = []
# 			for p in pron:
# 				sound = p[soundIndex]
# 				if sound not in soundList:
# 					soundList.append(sound)
# 			phraseSounds.append(soundList)


# 	for s in phraseSounds:
# 		print s



# def processCorpus():
# 	lines = sentence.splitlines()
# 	phrase = ''
# 	for i in range(len(lines)):
# 		phrase = phrase + lines[i]
# 		if ((i + 1) % phrase_len is 0):
# 			processPhrase(phrase)
# 			phrase = ''

# processCorpus()

# # Extract list of words


# pairs = []
# for w in words:





# for pair in pairs: print(pair)