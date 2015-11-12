import probabilisticState as ps

class pTrieState(ps.ProbabilisticState):

    def __init__(self, name, outedges, candFlag, testFlag):
        ps.ProbabilisticState.__init__(self, name, outedges)
        self.candidacy = candFlag
        self.tested = testFlag
        
    def nextCandidate(self, name, tStates):
        if self.candFlag:
            return self
        else:
            a = name[0]
            sName = self.nextStateFromEdge(a)
            names = [x.name for x in tStates]
            s = tStates[names.index(sName)]
            tStatesNew = [x for x in tStates if x.name != s.name]
            return s.nextCandidate(name[1:], tStatesNew)