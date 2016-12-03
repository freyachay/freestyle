import generation
import searchUtil

# ********* Creating search problem *********
class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        return self.query

    def isEnd(self, state):
        return (len(state) == 0)

    def succAndCost(self, state):
        results = []

        for i in range(len(state) + 1):
            results.append((state[:i], state[i:], self.unigramCost(state[:i])))

        return results

# ************************************

def costFunction:
	return 8

# *********** Solve search problem ******

def solve(startGram, unigramCost):
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(startGram, costFunction))
    return ' '.join(ucs.actions)


# ************************************

