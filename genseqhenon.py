#!/usr/bin/env
import probabilisticGraph as pg
g = pg.ProbabilisticGraph([],[])
for L in range(6,14,2):
    print L
    g.parseGraphFile("./Resultados/graph_henon_generated_L"+str(L)+"_NoMoore.txt")
    w = g.stateNamed("1111")
    s = g.generateSequence(10000000, w)
    f1 = "./Resultados/sequence_henon_generated_L"+str(L)+"_10000000_NoMoore.txt"
    f = open(f1,'w')
    f.write(s)
    f.close()   
    g.parseGraphFile("./Resultados/graph_henon_generated_L"+str(L)+".txt")
    w = g.stateNamed("1111")
    s = g.generateSequence(10000000, w)
    f1 = "./Resultados/sequence_henon_generated_L"+str(L)+"_10000000.txt"
    f = open(f1,'w')
    f.write(s)
    f.close()  
g.parseGraphFile("./Resultados/graph_henon_crissis.txt")
w = g.stateNamed("1111")
d = g.generateSequence(10000000, g.stateNamed("1111"))
d = d[:10000000]
f = open("./Resultados/sequence_henon_crissis.txt", 'w')
f.write(d)
f.close()
