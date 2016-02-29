#!/usr/bin/env
import probabilisticGraph as pg
import partition as pt
import partitionset as ps
import graphMinimization as gm
L = 6
g = pg.ProbabilisticGraph([],[])
g.parseGraphFile("./Resultados/graph_evenshift_10000000_L15.txt")
w = g.stateNamed("0")
Q = g.createInitialPartition(w, L, 0.95, "chi-squared")
P = []
for q in Q:
    p = q.pop(0)
    p1 = pt.Partition(p)
    while q:
        p1.addToPartition(q.pop(0))
    P.append(p1)    
PS = ps.PartitionSet(P)
g = g.removeUnreachableStates()
w = [x for x in g.states if len(x.name) < L]
g = pg.ProbabilisticGraph(w, g.alphabet)
gp = gm.moore(PS, g)
len(gp.partitions)
h = gp.recoverGraph(g)
