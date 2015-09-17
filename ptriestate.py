import probabilisticState as ps

class pTrieState(ps.ProbabilisticState):

    def __init__(self, name, outedges, candFlag):
        ps.ProbabilisticState.__init__(self, name, outedges)
        self.candFlag = candFlag
        
    def nextCandidate(self, name, tStates):
        if self.candFlag:
            return self
        else:
            a = name[0]
            sName = self.nextStateFromEdge(a)
            names = [x.name for x in tStates]
            s = tStates[names.index(sName)]
            return s.nextCandidate(name[1:], tStates.remove(s))
