import graph
import obtainstat
import probabilisticState
from scipy import stats

class ProbabilisticGraph(Graph):
    def __init__(self, states, alphabet):
        Graph.__init__(self, states, alphabet)
        
    def compareMorphs(stateA, stateB, alpha, test):
        morphA = [x[3] for x in stateA.outedges]
        morphB = [x[3] for x in stateB.outedges]
        if test == "chi-squared":
            [X, p] = stats.chisquare(morphA, morphB)         
        else if test == "ks":
            [KS, p] = stats.ks_2samp(morphA, morphB)
        return [p < alpha, p]   
        
        
        
