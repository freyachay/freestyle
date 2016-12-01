import nltk
import fmdict
import collections
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

sentence = "Unawareness I am sitting,\n at a table with!\n a water bottle \n Merrily we go"
mainDict = cmudict.dict()
extraDict = fmdict.extraDict

phrase_len = 2

# Takes in a word. Looks it up in either extraDict or mainDict and returns list of pronunciations
# (list of lists of sounds)
def getPron(word):
	# Check fm dict
	if word.lower() in extraDict.keys():
		return [extraDict[word.lower()]]
	# Look in cmudict
	if word.lower() in mainDict.keys():
		return mainDict[word.lower()]
	return None

def containsDigit(string):
	return any(char.isdigit() for char in string)

# This takes in a phrase (list of words) and returns a list of syllables made up of sounds.
def getSyllables(phrase):
	syllables = collections.defaultdict(list)
	currentSyl = []

	# For each pronunciation
	globalSylIndex = 0
	localSylIndex = 0
	for word in phrase:
		for pronunciation in getPron(word):
			localSylIndex = globalSylIndex	
			for sound in pronunciation:
				currentSyl.append(sound)
				if (containsDigit(sound)):
					prev = syllables[localSylIndex]
					if currentSyl not in prev:
						prev.append(currentSyl)
						syllables[localSylIndex] = prev

					localSylIndex += 1
					currentSyl = []

			if currentSyl is not []:
				lastSyl = syllables[localSylIndex - 1]
				lastPron = lastSyl[len(lastSyl)-1]
				for sound in currentSyl:
					lastPron.append(sound)

				if lastPron not in lastSyl:
					lastSyl[len(lastSyl)-1] = lastPron
					syllables[localSylIndex - 1] = lastSyl
				currentSyl = []
				
		globalSylIndex = localSylIndex
	return syllables

# def getRhymeScore(pron1, pron2):
# 	return 1



def processPhrase(phrase):
	tokens = wordpunct_tokenize(phrase)
	punct = ['.', ',', '!', ':', ';']
	words = [word for word in tokens if word not in punct]
	return words


# 	for s in phraseSounds:
# 		print s
def updateRhymeDist(phraseSylDict):
	for k, v in phraseSylDict.iteritems():
		print("{}: {}").format(k, v)
	print("\n")


def processCorpus():
	lines = sentence.splitlines()
	phrase = ''
	for i in range(len(lines)):
		phrase = phrase + lines[i]
		if ((i + 1) % phrase_len is 0):
			print(processPhrase(phrase))
			phraseSylDict = getSyllables(processPhrase(phrase))
			updateRhymeDist(phraseSylDict)
			phrase = ''

processCorpus()

# # Extract list of words


# pairs = []
# for w in words:





# for pair in pairs: print(pair)