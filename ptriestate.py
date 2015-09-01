import probabilisticState as ps

class pTrieState(ps.ProbabilisticState):

    def __init__(self, name, outedges, candFlag):
        ps.ProbabilisticState(self, name, outedges)
        self.candFlag = candFlag
        
    def nextCandidate(self, states, name):
        if self.candFlag:
            return self
        else:
            a = name[0]
            sName = self.nextFromLetter(a)
            names = [x.name for x in states]
            s = states[names.index(sName)]
            remainingStates = list(states)
            return s.nextCandidate(remainingStates.remove(s),name[1:])
