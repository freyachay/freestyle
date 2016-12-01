import nltk
import fmdict
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

sentence = "Unawareness I am sitting, at a table with! a water bottle \n Merrily we go"
mainDict = cmudict.dict()
extraDict = fmdict.extraDict

# Given 2 pronunciations, do these words rhyme?
def rhymeScore(pron1, pron2):



# Extract list of words
tokens = wordpunct_tokenize(sentence)
punct = ['.', ',', '!', ':', ';']
words = [word for word in tokens if word not in punct]

pairs = []
for w in words:
	# Check fm dict
	if w.lower() in extraDict.keys():
		pron = extraDict[w.lower()]
		pairs.append((w, pron))
		continue

	# Look in cmudict
	if w.lower() in mainDict.keys():
		pron = mainDict[w.lower()]
		pairs.append((w, pron))




for pair in pairs: print(pair)