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

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    print(ucs.actions)
    return ' '.join(ucs.actions)

# ************************************

