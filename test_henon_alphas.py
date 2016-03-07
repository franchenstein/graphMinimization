#!/usr/bin/env
import probabilisticGraph as pg
import partition as pt
import partitionset as ps
import graphMinimization as gm
import crissis as cr
g = pg.ProbabilisticGraph([],[])
L = 10
alpharange = [0.9, 0.95, 0.99]
for alpha in alpharange:
    g.parseGraphFile("./Resultados/graph_henon_L15.txt")
    w = g.stateNamed("1111")
    Q = g.createInitialPartition(w, L, alpha, "chi-squared")
    P = []
    for q in Q:
        p = q.pop(0)
        p1 = pt.Partition(p)
        while q:
            p1.addToPartition(q.pop(0))
        P.append(p1)    
    PS = ps.PartitionSet(P)
    h = PS.recoverGraph(g)
    f1 = "./Resultados/graph_henon_generated_alpha"+str(alpha)+"_NoMoore.txt"
    h.saveGraphFile(f1)
    d = h.generateSequence(10000000, h.stateNamed("1111"))
    f1 = "./Resultados/sequence_henon_generated_alpha"+str(alpha)+"_10000000_NoMoore.txt"
    f = open(f1,'w')
    f.write(d)
    f.close()   
    g = g.removeUnreachableStates()
    w = [x for x in g.states if len(x.name) < L]
    g = pg.ProbabilisticGraph(w, g.alphabet)
    gp = gm.moore(PS, g)
    h = gp.recoverGraph(g)
    f1 = "./Resultados/graph_henon_generated_L"+str(L)+".txt"
    h.saveGraphFile(f1)
    d = h.generateSequence(10000000, h.stateNamed("1111"))
    d = d[:10000000]
    f1 = "./Resultados/sequence_henon_generated_alpha"+str(alpha)+"_10000000.txt"
    f = open(f1,'w')
    f.write(d)
    f.close()
    #Crissis:
    g.parseGraphFile("./Resultados/graph_henon_L15.txt")
    w = g.stateNamed("1111")
    c = cr.crissis(w, g, alpha, "chi-squared")
    f = "./Resultados/graph_henon_crissis_alpha_"+str(alpha)+".txt"
    c.saveGraphFile(f)
    d = c.generateSequence(10000000, c.stateNamed("1111"))
    f1 = "./Resultados/sequence_henon_crissis_alpha_"+str(alpha)+".txt"
    f = open(f1, 'w')
    f.write(d)
    f.close()
      
