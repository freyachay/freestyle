import nltk
import fmdict
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

sentence = "Unawareness I am sitting,\n at a table with!\n a water bottle \n Merrily we go"
mainDict = cmudict.dict()
extraDict = fmdict.extraDict

phrase_len = 2

# Given 2 pronunciations, do these words rhyme?

def getRhymeScore(pron1, pron2):
	return 1

def getPron(word):
	# Check fm dict
	if word.lower() in extraDict.keys():
		return [extraDict[word.lower()]]
	# Look in cmudict
	if word.lower() in mainDict.keys():
		return mainDict[word.lower()]
	return None

def processPhrase(phrase):
	tokens = wordpunct_tokenize(sentence)
	punct = ['.', ',', '!', ':', ';']
	words = [word for word in tokens if word not in punct]

	# List of lists of possible pronunciations for each sound in phrase
	phraseSounds = []

	# For each word in phrase
	for word in words:
		pron = getPron(word)
		if pron is None: continue
		for soundIndex in range(len(pron[0])):
			soundList = []
			for p in pron:
				sound = p[soundIndex]
				if sound not in soundList:
					soundList.append(sound)
			phraseSounds.append(soundList)


	for s in phraseSounds:
		print s



def processCorpus():
	lines = sentence.splitlines()
	phrase = ''
	for i in range(len(lines)):
		phrase = phrase + lines[i]
		if ((i + 1) % phrase_len is 0):
			processPhrase(phrase)
			phrase = ''

processCorpus()

# # Extract list of words


# pairs = []
# for w in words:





# for pair in pairs: print(pair)