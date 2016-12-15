
import nltk
import random
import collections
import pickle
import constants
import generation
from numpy.random import choice
from nltk.util import ngrams
from collections import Counter
from collections import defaultdict

# Model global variables
styleName = "Hamilton"

def dd():
	return defaultdict(float)

f = open(styleName.lower() + "Lyrics.txt")
contents = f.read()
lines = contents.splitlines()
numLines = len(lines)

start = random.randrange(numLines)
end = start + 51
while end > numLines:
	start = random.randrange(numLines)
	end = start + 50

generatedText = '\n'.join(lines[start:end])
print(generatedText)

distance, fluencyScore = generation.evaluate(styleName, generatedText, False)
print("Distance: {}".format(distance))
print("Fluency: {}".format(fluencyScore))
print("\n")
	
