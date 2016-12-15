import generation
from collections import defaultdict

def dd():
	return defaultdict(float)

styleName = "Hamilton"
f = open("golden.txt")
contents = f.read()

rhymeScore, fluencyScore = generation.evaluate(styleName, contents, False)
print("Rhyme score: {}".format(rhymeScore))
print("Fluency score: {}".format(fluencyScore))
print("\n")
	
