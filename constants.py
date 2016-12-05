
styleNames = ['Chance']

# For gram model (used in model and generation)
n = 2

# Number of lines per phrase (used in model and generation)
phraseLen = 1

# Number of phrases to generate (used in generation)
numPhrases = 2

# How probable must a rhyme be to count as needing to rhyme? (used in generation)
rhymeThresh = 0.05 

# Constants for generation by search
rhymeWeight = 10
pruningConstant = 10