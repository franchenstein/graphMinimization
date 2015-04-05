class State:
    
    def __init__(self, name, outedges):
        self.name = name
        self.outedges = outedges
        
    def nextStateFromEdge(self, letter):
        matches = [x[1] for x in self.outedges if x[0] == letter]
        return matches[0]
        
    def edgeThatLeadsToState(self, stateName):
        matches = [x[0] for x in self.outedges if x[1] == stateName]
        return matches[0]    
