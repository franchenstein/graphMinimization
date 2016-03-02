#!/usr/bin/env
import probabilisticGraph as pg
import partition as pt
import partitionset as ps
import graphMinimization as gm
import crissis as cr
g = pg.ProbabilisticGraph([],[])
for L in range(4,12,2):
    print L
    g.parseGraphFile("./Resultados/graph_trishift_asok_L15.txt")
    w = g.stateNamed("00")
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
    f1 = "./Resultados/graph_trishift_generated_L"+str(L)+"_NoMoore.txt"
    h.saveGraphFile(f1)
    d = h.generateSequence(10010000, h.stateNamed("00"))
    d = d[:10000000]
    f1 = "./Resultados/sequence_trishift_generated_L"+str(L)+"_10000000_NoMoore.txt"
    f = open(f1,'w')
    f.write(d)
    f.close()   
    g = g.removeUnreachableStates()
    w = [x for x in g.states if len(x.name) < L]
    g = pg.ProbabilisticGraph(w, g.alphabet)
    gp = gm.moore(PS, g)
    h = gp.recoverGraph(g)
    f1 = "./Resultados/graph_trishift_generated_L"+str(L)+".txt"
    h.saveGraphFile(f1)
    d = h.generateSequence(10010000, h.stateNamed("00"))
    d = d[:10000000]
    f1 = "./Resultados/sequence_trishift_generated_L"+str(L)+"_10000000.txt"
    f = open(f1,'w')
    f.write(d)
    f.close()
    #Crissis:
    g.parseGraphFile("./Resultados/graph_trishift_asok_L15.txt")
    w = g.stateNamed("00")
    c = cr.crissis(w, g, 0.95, "chi-squared")
    c.saveGraphFile("./Resultados/graph_trishift_crissis.txt")
    d = c.generateSequence(10001000, c.stateNamed("00"))
    d = d[:10000000]
    f = open("./Resultados/sequence_trishift_crissis.txt", 'w')
    f.write(d)
    f.close()
      
