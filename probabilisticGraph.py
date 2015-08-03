import graph
import obtainstat
import probabilisticState
from scipy import stats

class ProbabilisticGraph(graph.Graph):
    def __init__(self, states, alphabet):
        graph.Graph.__init__(self, states, alphabet)
        
    def compareMorphs(self, stateA, stateB, alpha, test):
        morphA = [float(x[2]) for x in stateA.outedges]
        morphB = [float(x[2]) for x in stateB.outedges]
        if test == "chi-squared":
            [X, p] = stats.chisquare(morphA, morphB)         
        elif test == "ks":
            [KS, p] = stats.ks_2samp(morphA, morphB)
        return [p > alpha, p]   
        
        
        
