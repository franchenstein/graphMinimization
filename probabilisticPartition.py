import partition
import probabilisticState
import numpy

class ProbabilisticPartition(partition.Partition):
    
    def __init__(self, state):
        #A new partition is initialized with just one state:
        self.name = state.name
        self.outedges = state.outedges
        self.size = 0 if not state.name else 1
        
    def morph(self):
        alph = []
        alph = list(set([x[0] for x in self.outedges]))
        newEdges = []
        for a in alph:
            currentEdges = [edge for edge in self.outedges if edge[0] == a]
            probs = [float(e[2]) for e in currentEdges]
            newEdge = (a,"place-holder", numpy.mean(probs))
            newEdges.append(newEdge)
        return newEdges
