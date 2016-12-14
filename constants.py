
styleNames = ['Hamilton']


# *********** Greedy

# For gram model (used in model and generation)
<<<<<<< HEAD
n = 2

# Number of lines per phrase (used in model and generation)
<<<<<<< HEAD
phraseLen = 4

# Number of phrases to generate (used in generation)
numPhrases = 10

# How probable must a rhyme be to count as needing to rhyme? (used in generation)
rhymeThresh = 0.01
numPhrases = 30
=======
phraseLen = 1

# Number of phrases to generate (used in generation)
numPhrases = 1

# How probable must a rhyme be to count as needing to rhyme? (used in generation)
rhymeThresh = 0.01
>>>>>>> f3e37350b9da14c139d0d50bc69863a391bc47cd
=======
# n = 2
>>>>>>> 7516ec9bab6b32d3b25d8042a10b05dee1a4dffe

# # Number of lines per phrase (used in model and generation)
# phraseLen = 2

# # Number of phrases to generate (used in generation)
# numPhrases = 3



# ********** Search

# For gram model (used in model and generation)
n = 2

# Number of lines per phrase (used in model and generation)
phraseLen = 1

# Number of phrases to generate (used in generation)
numPhrases = 8

maxLineLen = 8

# Pruning -- how many of each do we branch?
pruneFluency = 5
pruneRhyming = 5

lastSylWeight = 3