import ptriestate as pts
import probabilisticGraph as pg

class CandidacyTrie(pg.ProbabilisticGraph):
    
    def __init__(self, states, alphabet):
        pStates = []
        for s in states:
            rName = s.name[::-1]
            rOutedges = []
            for e in s.outedges:
                redge = (e[0], e[1][::-1], e[2])
                rOutedges.append(redge)
            p = pts.pTrieState(rName, rOutedges, False, False)
            pStates.append(p)
        pg.ProbabilisticGraph.__init__(self, pStates, alphabet)
        
    # def expandState(self, s, g):
    #     if s.candFlag:
    #         s.candFlag = False
    #         newNames = []
    #         for a in self.alphabet:
    #             if s.name == "e":
    #                 newName = a
    #             else:
    #                 newName = a + s.name
    #             names = [x.name for x in g.states]
    #             newEdges = g.states[names.index(newName[::-1])].outedges
    #             newState = pts.pTrieState(newName, newEdges, True)
    #             self.states.append(newState)
    #             newNames.append(newName[::-1])
    #             #still need to consider case when last nodes are reached
    #         return newNames
    #     else:
    #         a = []
    #         for i in self.alphabet:
    #             a.append(s.nextStateFromEdge(a).name[::-1])
    #         return a

    def validStates(self):
        s = [x for x in self.states if (x.candidacy == True) and (x.tested == False)]
        s.sort(key=lambda x: len(x.name))
        return s

    # def root(self):
    #     r = pg.ProbabilisticGraph.root(self)
    #     return r

    def expand(self, s, l):
        for state in self.states:
            if state.name == s.name:
                f = state
                f.candidacy = False
        exp = pg.ProbabilisticGraph.expand(self, f)
        for e in exp:
            if e.nameLength() < l:
                e.candidacy = True
        return exp

    def markUntested(self):
        for s in self.states:
            if s.candidacy == True:
                s.tested = False

    def markTested(self, s):
        for state in self.states:
            if state.name == s.name:
                state.tested = True

    def isSuffix(self, full, candidate):
        if candidate == 'e':
            return True
        else:
            l = len(full) - len(candidate)
            partial = full[::-1]
            a = range(0,len(candidate))
            aux = self.root()
            for i in a:
                newStateName = aux.nextStateFromEdge(partial[i])
                aux = self.stateNamed(newStateName)
                if aux == None:
                    return False
            return (aux.name is candidate and aux.candidacy)

    def shortestValidSuffix(self, name):
        n = name [::-1]
        aux = self.root()
        i = 0
        while (aux.candidacy is False) and (i < len(n)):
            newStateName = aux.nextStateFromEdge(n[i])
            aux = self.stateNamed(newStateName)
            i += 1
            if aux is None:
                return aux
        return aux.name