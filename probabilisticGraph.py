import graph
import obtainstat
import probabilisticState
from scipy import stats

class ProbabilisticGraph(graph.Graph):
    def __init__(self, states, alphabet):
        graph.Graph.__init__(self, states, alphabet)
        
    def compareMorphs(self, edgesA, edgesB, alpha, test):
        morphA = [float(x[2]) for x in edgesA]
        morphB = []
        #Loop to guarantee the probability distributions are in the same order:
        for a in [x[0] for x in edgesA]:
            for x in edgesB:
                if x[0] == a:
                    morphB.append(x[2]) 
        if morphA == morphB:
            return [True, 1.0]
        else: 
            if test == "chi-squared":
                [X, p] = stats.chisquare(morphA, morphB)         
            elif test == "ks":
                [KS, p] = stats.ks_2samp(morphA, morphB)
            return [p >= alpha, p]
