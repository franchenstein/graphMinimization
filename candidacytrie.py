import ptriestate as pts
import probabilisticGraph as pg

class candidacyTrie(pg.ProbabilisticGraph):
    
    def __init__(self, states, alphabet):
        pg.ProbabilisticGraph(states, alphabet)
        
    def expandState(self, stateName, outedges):
        sNames = [x.names for x in self.states]
        s = self.states[sNames.index(stateName)]
        s.outedges = outedges
        s.candFlag = False
        for a in self.alphabet:
            newState = pts.pTrieState(a + stateName, [], True)
            self.states.append(newState)
            #still need to consider case when last nodes are reached
