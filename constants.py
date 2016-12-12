
styleNames = ['Hamilton']


# *********** Greedy

# For gram model (used in model and generation)
# n = 2

# # Number of lines per phrase (used in model and generation)
# phraseLen = 2

# # Number of phrases to generate (used in generation)
# numPhrases = 3

# # How probable must a rhyme be to count as needing to rhyme? (used in generation)
# rhymeThresh = 0.05



# ********** Search

# For gram model (used in model and generation)
n = 2

# Number of lines per phrase (used in model and generation)
phraseLen = 1

# Number of phrases to generate (used in generation)
numPhrases = 1

# Pruning -- how many of each do we branch?
pruneFluency = 3
pruneRhyming = 3

lastSylWeight = 3