import ptriestate as pts
import probabilisticGraph as pg

class CandidacyTrie(pg.ProbabilisticGraph):
    
    def __init__(self, states, alphabet):
        pg.ProbabilisticGraph.__init__(self, states, alphabet)
        
    def expandState(self, s, g):
        s.candFlag = False
        newNames = []
        for a in self.alphabet:
            if s.name == "e":
                newName = a
            else:
                newName = a + s.name
            names = [x.name for x in g.states]
            newEdges = g.states[names.index(newName[::-1])].outedges
            newState = pts.pTrieState(newName, newEdges, True)
            self.states.append(newState)
            newNames.append(newName[::-1])
            #still need to consider case when last nodes are reached
        return newNames
