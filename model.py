import nltk
import fmdict
import pickle
from collections import defaultdict
from nltk.util import ngrams
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize, RegexpTokenizer

# Global variables
sentence = "Hey there \n bear the be this care \n Yes \n I am a care bear mess all guy sky"
mainDict = cmudict.dict()
extraDict = fmdict.extraDict
boringWords = ["the","be","to","of","and","a","in","that","have", \
				"I","it","for","not","on","with","he","as","you","do", \
				"at","this","but","his","by","from","they","we","say", \
				"her","she","or","an","will","my","one","all","there", \
				"their","what","so","who","if","them","yeah"]

n = 2
phrase_len = 2

# These will be populated after running
def dd():
	return defaultdict(float)

rhymeDist = defaultdict(dd)
lineLenDist = defaultdict(float)
gramDict = defaultdict(list)
rhymingDictionary = defaultdict(set)



# ************* Helpers ***********

# Takes a string and returns a list of words, seperated by punctuation (but not apostrophes or dashes)
def processPhrase(phrase):
	tokenizer = RegexpTokenizer('[\'\w\-]+')
	tokens = tokenizer.tokenize(phrase)
	punct = ['.', ',', '!', ':', ';']
	words = [word for word in tokens if word not in punct]
	return words

# **********************************



# ************* Rhyme distribution ************

# Returns true of string contains a digit (useful for identifying stressed sounds)
def containsDigit(string):
	return any(char.isdigit() for char in string)

# Takes in a word. Looks it up in either extraDict or mainDict and returns list of pronunciations
# (list of lists of sounds)
def getPron(word):
	# Check fm dict
	if word.lower() in extraDict.keys():
		return [extraDict[word.lower()]]
	# Look in cmudict
	if word.lower() in mainDict.keys():
		return mainDict[word.lower()]
	
	# ****** Print words that are in neither dictionary
	# print(word)
	return None

# This takes in a phrase (list of words) and returns a list of syllables made up of sounds.
def getSyllables(phrase):
	syllables = defaultdict(list)
	currentSyl = []

	# For each pronunciation
	globalSylIndex = 0
	localSylIndex = 0
	for word in phrase:
		possibleProns = getPron(word)
		if possibleProns is None: continue

		for pronunciation in possibleProns:
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

# Takes in 2 pronunciations of syllables (lists of sounds), returns 
# whether or not they "rhyme" (rhyming = shared stressed vowel and suffix)
def sylRhymes(syl1, syl2):
	# Reject repetition
	if (syl1 == syl2): return False

	# Get stressed syllable and suffix from syl1
	stressed1 = [s for s in syl1 if containsDigit(s)][0] # We know there will only be one stressed syl
	stressIndex1 = syl1.index(stressed1)
	suffix1 = syl1[stressIndex1 + 1:]

	# Same for syl2
	stressed2 = [s for s in syl2 if containsDigit(s)][0] # We know there will only be one stressed syl
	stressIndex2 = syl2.index(stressed2)
	suffix2 = syl2[stressIndex2 + 1:]

	return (stressed1 == stressed2) and (suffix1 == suffix2)

# Counts how many times each position (syllable) rhymes with each previous position in the phrase
def updateRhymeDistCounts(phraseSylDict):
	for pos1, prons in phraseSylDict.iteritems():
		for pos2 in range(pos1):
			found = False
			prevProns = phraseSylDict[pos2]
			for pron1 in prons:
				for pron2 in prevProns:
					if (sylRhymes(pron1, pron2)):
						found = True
						(rhymeDist[pos1])[pos2] += 1
						break
				if found: break

# Normalizes rhymeDist based on number of phrases
def normalizeRhymeDist(phraseCount):
	for pos, count in rhymeDist.iteritems():
		for k, v in count.iteritems():
			(rhymeDist[pos])[k] = v/phraseCount

# ****************************************************




# ********** Line count distribution *******

# Takes a line, updates line length distribution counts
def updateLineDistCounts(line):
	syllables = getSyllables(processPhrase(line))
	lineLenDist[len(syllables)] += 1

# Normalizes lineLenDist based on number of lines
def normalizeLineDist(lineCount):
	for length, count in lineLenDist.iteritems():
		lineLenDist[length] = count/lineCount

# ****************************************





# ***** N-grams ******

# Takes in a list of words, returns a list of n-grams
def generate_grams(words):
    gramList = []
    for ngram in ngrams(words, n):
        gramList.append(' '.join(str(i) for i in ngram))
    return gramList

# Creates list of n-grams from text (contents), updates dictionary mapping n-grams to successor words
def buildGramDict(contents):
	grams = generate_grams(processPhrase(contents))
	for gram in grams:
		words = gram.split()
		key = ()
		for i in range(n-1):
			key = key + (words[i],)

		gramDict[key].append(words[n-1])

# ************************





# **************** Rhyming dictionary *********

# Populates rhymingDictionary which maps the rhyming part of a syllable to words that contain
# it in their first syllable.
def buildRhymingDict(contents):
	words = processPhrase(contents)
	for word in words:
		print(word)
		if word in boringWords: continue
		syllables = getSyllables([word])
		for pron in syllables[0]:
			print(pron)
			key = ""
			# Get stressed syllable and suffix from syl1
			stressed = [s for s in pron if containsDigit(s)][0] # We know there will only be one stressed syl
			stressIndex = pron.index(stressed)
			suffix = pron[stressIndex + 1:]
			key = stressed + ''.join(suffix)
			print(key)
			rhymingDictionary[key].add(word)
			print("\n")


	# words = processPhrase(contents)
	# for i in range(len(words)):
	# 	word1 = words[i]
	# 	if word1 in boringWords: continue
	# 	for j in range(i):
	# 		word2 = words[j]
	# 		if word2 in boringWords: continue
	# 		if word1 == word2: continue
	# 		if rhymesWith(word1, word2): 
	# 			rhymingDictionary[word1].add(word2)
	# 			rhymingDictionary[word2].add(word1)


# **********************************************





# ***** Main script *****

f = open('chanceLyrics.txt')
contents = f.read()

# buildGramDict(sentence)
buildRhymingDict(sentence)
for k, v in rhymingDictionary.iteritems():
	print("{}, {}".format(k, v))

# lines = sentence.splitlines()
# phrase = ''
# lineCount = 0
# phraseCount = 0
# for i in range(len(lines)):
# 	if lines[i] == '': continue

# 	lineCount += 1
# 	updateLineDistCounts(lines[i])
# 	phrase = phrase + " " + lines[i]
# 	if ((i + 1) % phrase_len is 0):
# 		phraseCount += 1
# 		phraseSylDict = getSyllables(processPhrase(phrase))
# 		updateRhymeDistCounts(phraseSylDict)
# 		phrase = ''
# normalizeLineDist(lineCount)
# normalizeRhymeDist(phraseCount)

# # Write model to file (rhymeDist, lineLenDist, gramDict)
# pickle.dump(rhymeDist, open("rhymeDist.p", "wb"))
# pickle.dump(lineLenDist, open("lineLenDist.p", "wb"))
# pickle.dump(gramDict, open("gramDict.p", "wb"))
# print(rhymeDist)
# print(lineLenDist)
# print(gramDict)









