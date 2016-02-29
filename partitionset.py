import partition
import probabilisticGraph as pg
import probabilisticState as ps

class PartitionSet:
    
    def __init__(self, partitions):
        self.partitions = partitions
        
    def updatePartitionsEdges(self):
        for partToUpdate in self.partitions:
            for otherParts in self.partitions:
                partToUpdate.updateEdges(otherParts)
                
    def recoverGraph(self, g):
        S = [g.stateNamed(p.name[0]) for p in self.partitions]
        states = []
        for s in S:
            oe = []
            for a in g.alphabet:
                t = g.stateNamed(s.nextStateFromEdge(a))
                if t != None:
                    for p in self.partitions:
                        if t.name in p.name:
                            for e in s.outedges:
                                if e[0] == a:
                                    newedge = (a, p.name[0], e[2])
                                    oe.append(newedge)
                                    break
                            break
            u = ps.ProbabilisticState(s.name, oe)
            states.append(u)
        h = pg.ProbabilisticGraph(states, g.alphabet)
        return h
                        
                        
        
