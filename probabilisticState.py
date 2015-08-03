import state

class ProbabilisticState(state.State):
    
    def __init__(self, name, outedges):
        state.State.__init__(self, name, outedges)
        
    def probToNextState(self, stateName):
        matches = [x[2] for x in self.outedges if x[1] == stateName]
        return matches[0]
        
    def probToNextLetter(self, letter):
        matches = [x[2] for x in self.outedges if x[0] == letter]
        return matches[0]
