#!/usr/bin/env
import sys, getopt
import obtainstat as os
import probabilisticGraph as pg
import multiprocessing as mp
import partition as pt
import partitionset as ps
import graphMinimization as gm
import crissis as cr
import dmarkov

#Auxiliary functions:
def generateAndSaveSequences(g, w, t, L, l, alpha, seqType):
    d = g.generateSequence(l, w)
    path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+seqType+".txt"
    f = open(path, 'w')
    f.write(d)
    f.close()  
    
def readSequenceFile(path): 
    f = open(path)
    s = ""
    for l in f.readlines():
        if l[-1] == '\n':
            s += l[:-1]
        else:
            s += l
    f.close()
    s = list(s)
    s = [int(x) for x in s]
    return s
    
def stringToResult(s):
    x = s[:-1].split(',')
    y = [float(i) for i in x]
    
def resultToString(r):
    l = [str(x) for x in r]
    l = ','.join(l) + '\n'
    return l
    
def defineRanges(l, a):
    if l:
        lrange = range(6, 14 ,2)
    else:
        lrange = [10]
      
    if a:
        alpharange = [0.85, 0.9, 0.95, 0.99]
    else:
        alpharange = [0.95]
        
    return [lrange, alpharange]
    
#Main functions:
def generateGraphs(t, ranges):
    g = pg.ProbabilisticGraph([],[])
    print "Opening original tree\n"
    if t == "henon":
        g.parseGraphFile("./Resultados/graph_henon_L15.txt")
        w = g.stateNamed("1111")
    elif t == "even":
        g.parseGraphFile("./Resultados/graph_evenshift_10000000_L15.txt")
        w = g.stateNamed("0") 
    elif t == "tri":
        g.parseGraphFile("./Resultados/graph_trishift_10000000_L15.txt")
        w = g.stateNamed("00") 
    
    #D-Markov:    
    print "Creating D-Markov Graph\n"
    dm = dmarkov.DMarkov(g, 9)
    path = "./Resultados/graph_"+t+"_dmarkov_9.txt"
    dm.saveGraphFile(path)  
        
    lrange, alpharange = ranges
    
    print "Creating partitions\n"
    for alpha in alpharange:
    	print "alpha:"
    	print alpha
        for L in lrange:
	    print "L:"
	    print L
            Q = g.createInitialPartition(w, L, alpha, "chi-squared")
            P = []
            for q in Q:
                p = q.pop(0)
                p1 = pt.Partition(p)
                while q:
                    p1.addToPartition(q.pop(0))
                P.append(p1)
            PS = ps.PartitionSet(P)
            #No Moore sequence and graph:
	    print "Generating NoMoore graphs\n"
            h = PS.recoverGraph(g)
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
            h.saveGraphFile(path)
            
            #With Moore sequence and graph:
 	    print "Generating graphs after Moore\n"
            i = g.removeUnreachableStates()
            shortStates = [x for x in i.states if len(x.name) < L]
            i = pg.ProbabilisticGraph(shortStates, i.alphabet)
            ip = gm.moore(PS, i)
            j = ip.recoverGraph(i)
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
            j.saveGraphFile(path)
        #CRiSSiS:
	print "Generating CRiSSiS graph\n"
        c = cr.crissis(w, g, alpha, "chi-squared")
        path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        c.saveGraphFile(path)
    return
    
def generateSequences(t, ranges):
    g = pg.ProbabilisticGraph([], [])
    if t == "henon":
        wsyn = "1111"
    elif t == "tri":
        wsyn = "00"
        d = os.generate("tri", 10000000, [0.5, 0.8, 0.7])
        path = "./Resultados/sequence_trishift_original_10000000.txt"
        f = open(path, 'w')
        f.write(d)
        f.close()
    elif t == "even":
        wsyn = "0"
        d = os.generate("even", 10000000, [0.99])
        path = "./Resultados/sequence_evenshift_original_10000000.txt"
        f = open(path, 'w')
        f.write(d)
        f.close()
    
    lrange, alpharange = ranges
    
    #D-Markov:    
    path = "./Resultados/graph_"+t+"_dmarkov_9.txt"
    g.parseGraphFile(path)
    generateAndSaveSequences(g, g.states[0], t, 'X', 10000000, 'X', '_dmarkov9')
    
    for alpha in alpharange:
        for L in lrange:
            #No Moore:
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '_NoMoore')
            #With Moore:
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '')
        path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        g.parseGraphFile(path)
        generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '_crissis')    
    return
    
def compareSequences(t, l, a, ranges):
    if t == "henon":
        path = "../Sequencias/MH6.dat"
    elif t == "even":
        path = "./Resultados/sequence_evenshift_original_10000000.txt"
    elif t == "tri":
        path = "./Resultados/sequence_trishift_original_10000000.txt"
    s = []
    s.append(readSequenceFile(path))
    path = "./Resultados/sequence_"+t+"generated_L_X_alpha_X_dmarkov9.txt"
    s.append(readSequenceFile(path))
    
    lrange, alpharange = ranges
    
    #Opening files first. If error occurs here, no time was wasted processing
    #what will need to be processed again once this functions is ran again
    for alpha in alpharange:
        for L in lrange:
            #No Moore:
            path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
            s.append(readSequenceFile(path))
            #With Moore:
            path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
            s.append(readSequenceFile(path))
        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        s.append(readSequenceFile(path))
        
    #Once all sequences were obtained correctly, new loop to process them
    P = []
    P_cond = []
    H = []
    A = []
    K = []
    q = mp.Queue()
    for seq in s:
        p, alph = os.calcProbs(seq, 15, q)
        P.append(p)
        pcond = os.calcCondProbs(p, 15, alph)
        P_cond.append(pcond)
        h = os.calcCondEntropy(p, pcond, 15)
        H.append(h)
        a = os.autocorrelation(seq, 200)
        A.append(a)
        if seq is not s[0]:
            k = os.calcKLDivergence(P[0], p, 10)
            K.append(k)
        
    path = "./Resultados/entropies_"+t+".txt"
    f = open(path, 'w')
    for h in H:
        f.write(resultToString(h))
    f.close()
    
    path = "./Resultados/autocorrelations_"+t+".txt"
    f = open(path, 'w')
    for a in A:
        f.write(resultToString(a))
    f.close()
             
    path = "./Resultados/kldivergences_"+t+".txt" 
    if l:
        rng = ranges[0]
    if a:
        rng = ranges[1] 
    KLD = []
    k = K.pop(0)
    KLD.append([k for i in rng])
    k = K.pop()
    KLD.append([k for i in rng])
    count = 0
    kaux = []
    for k in K:
        if count < len(rng):
              kaux.append(k)
              k += 1
        else:
            KLD.append(kaux)
            k = 0
    f = open(path, 'w')
    for kld in KLD:
        f.write(resultToString(kld))
    f.close()
    
    return
            
def main(argv):
    t, g, s, l, a, c = readInput(argv)
    ranges = defineRanges(l, a)
    if g:
        generateGraphs(t, ranges)
    if s:
        generateSequences(t, ranges)
    if c:
    	compareSequences(t, l, a, ranges)
    return 0

def readInput(argv):
	t = ""
	s = True
	g = True
	a = True
	l = True
	c = True
	try:
		opts, args = getopt.getopt(argv, "ht:g:s:l:a:c", ["type=", "graph=", "sequence=", "L=", "alpha=", "compare="])
	except getopt.GetoptError:
		print 'test_generated_graph.py -t <type> -g <graph> -s <sequence> -l <L> -a <alpha> -c <compare>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'test_generated_graph.py -t <type> -g <graph> -s <sequence> -l <L> -a <alpha> -c <compare>'
			sys.exit()
		elif opt in ("-t", "--type"):
			t = arg
		elif opt in ("-g", "--graph"):
			if arg == 'True':
			    g = True
			else:
			    g = False
		elif opt in ("-s", "--sequence"):
			if arg == 'True':
			    s = True
			else:
			    s = False
		elif opt in ("-l", "--L"):
			if arg == 'True':
			    l = True
			else:
			    l = False
		elif opt in ("-a", "--alpha"):
			if arg == 'True':
			    a = True
			else:
			    a = False
		elif opt in ("-c","--compare"):
		    	if arg == 'True':
			    c = True
			else:
			    c = False
	return [t, g, s, l, a, c]

if __name__ == "__main__":
	main(sys.argv[1:])