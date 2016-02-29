#!/usr/bin/env
import probabilisticGraph as pg
import partition as pt
import partitionset as ps
import graphMinimization as gm
g = pg.ProbabilisticGraph([],[])
for L in range(4,14,2):
    print L
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
    h = PS.recoverGraph(g)
    f1 = "./Resultados/graph_evenshift_generated_L"+str(L)+"_NoMoore.txt"
    h.saveGraphFile(f1)
    d = h.generateSequence(10010000, h.stateNamed("0"))
    d = d[:10000000]
    f1 = "./Resultados/sequence_evenshift_generated_L"+str(L)+"_10000000_NoMoore.txt"
    f = open(f1,'w')
    f.write(d)
    f.close()   
    g = g.removeUnreachableStates()
    w = [x for x in g.states if len(x.name) < L]
    g = pg.ProbabilisticGraph(w, g.alphabet)
    gp = gm.moore(PS, g)
    h = gp.recoverGraph(g)
    f1 = "./Resultados/graph_evenshift_generated_L"+str(L)+".txt"
    h.saveGraphFile(f1)
    d = h.generateSequence(10010000, h.stateNamed("0"))
    d = d[:10000000]
    f1 = "./Resultados/sequence_evenshift_generated_L"+str(L)+"_10000000.txt"
    f = open(f1,'w')
    f.write(d)
    f.close()  
