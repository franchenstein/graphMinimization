#!/usr/bin/env
import sys, getopt
import obtainstat as obst
import probabilisticGraph as pg
import multiprocessing as mp
import partition as pt
import partitionset as ps
import graphMinimization as gm
import crissis as cr
import dmarkov
import os.path
import json

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

def openGraph(t, g):
    if t == "henon":
	g.parseGraphFile("./Resultados/graph_henon_L15.txt")
	w = g.stateNamed("1111")
    elif t == "even":
	g.parseGraphFile("./Resultados/graph_evenshift_10000000_L15.txt")
	w = g.stateNamed("0")
    elif t == "tri":
	g.parseGraphFile("./Resultados/graph_trishift_10000000_L15.txt")
	w = g.stateNamed("00")
    return [g, w]
    
#Main functions:
def generateGraphs(t, ranges):
    g = pg.ProbabilisticGraph([],[])
    print "Opening original tree\n"
    g, w = openGraph(t, g) 
    
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
	    g, w = openGraph(t, g)
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
        d = obst.generate("tri", 10000000, [0.5, 0.8, 0.7])
        path = "./Resultados/sequence_trishift_original_10000000.txt"
        f = open(path, 'w')
        f.write(d)
        f.close()
    elif t == "even":
        wsyn = "0"
        d = obst.generate("even", 10000000, [0.99])
        path = "./Resultados/sequence_evenshift_original_10000000.txt"
        f = open(path, 'w')
        f.write(d)
        f.close()
    
    lrange, alpharange = ranges
    
    print "Generating D-Markov Sequence"
    #D-Markov:    
    path = "./Resultados/graph_"+t+"_dmarkov_9.txt"
    g.parseGraphFile(path)
    generateAndSaveSequences(g, g.states[0], t, 'X', 10000000, 'X', '_dmarkov9')
    
    for alpha in alpharange:
	print "Alpha:"
	print alpha
        for L in lrange:
	    print "L:"
	    print L
            #No Moore:
	    print "Generating NoMoore Sequence"
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '_NoMoore')
            #With Moore:
	    print "Generating Sequence W/ Moore"
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '')
	print "Generating CRiSSiS Sequence"
        path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        g.parseGraphFile(path)
        generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '_crissis')    
    return

def computeProbabilities(t, s):
    print "Checking if available probabilities"
    path = "Resultados/probabilities_"+t+".json"
    if os.path.isfile(path):
        P = []
        P_cond = []
        f = open(path, 'r')
        P = json.load(f)
        f.close()
        path = "Resultados/conditional_probabilities_"+t+".json"
        f = open(path, 'r')
        P_cond = json.load(f)
        f.close()        
    else:        
        #Once all sequences were obtained correctly, new loop to process them
        P = []
        Alph = []
        q = mp.Queue()
        P_cond = []
        for seq in s:
            p, alph = obst.calcProbs(seq, 15, q)
            P.append(p)
            Alph.append(alph)
            pcond = obst.calcCondProbs(p, 15, alph)
        print "Saving Probabilities"
        path = "./Resultados/probabilities_"+t+".json"
        f = open(path, 'w')
        json.dump(P, f)
        f.close()
        print "Saving Conditional Probabilities"
        path = "./Resultados/conditional_probabilities_"+t+".json"
        f = open(path, 'w')
        json.dump(P_cond, f)
        f.close()
        
    return [P, P_cond]
    
def computeEntropies(t, P, P_cond):
    H = []
    print "Calculating Entropies"
    i = 0
    for p in P:
        h = obst.calcCondEntropy(p, P_cond[i], 15)
        i += 1
        H.append(h)
    print "Saving Entropies"
    path = "./Resultados/entropies_"+t+".txt"
    f = open(path, 'w')
    i = 1
    for h in H:
        print i
        i += 1
        f.write(resultToString(h))
    f.close()
    return H  
    
def computeAutocorrelation(t, s): 
    A = []
    for seq in s:
        a = obst.autocorrelation(seq,200)
        A.append(a)
    print "Saving Autocorrelations"
    path = "./Resultados/autocorrelations_"+t+".txt"
    f = open(path, 'w')
    i = 1
    for a in A:
        print i
        i += 1
        f.write(resultToString(a))
    f.close()
    return A
    
def computeKLD(t, P, a, l, ranges):
    print "Calculating Divergences"
    K = []
    lrange, alpharange = ranges
    #D-Markov KLD:
    p0 = P[0]
    pd = P[1]
    k = obst.calcKLDivergence(p0, pd, 10)
    if a:
        rng = range(0, len(alpharange))
        K.append([k for i in rng])
        knm = []
        km = []
        kc = []
        j = 1
        for i in rng:
            print j
            j += 1
            knm.append(obst.calcKLDivergence(p0, P[2+i], 10))
            km.append(obst.calcKLDivergence(p0, P[3+i], 10))
            kc.append(obst.calcKLDivergence(p0, P[4+i], 10))
        K.append(knm)
        K.append(km)
        K.append(kc)
    if l:
        rng = range(0, len(lrange))
        K.append([k for i in rng])
        knm = []
        km = []
        j = 1
        for i in rng:
            print j
            j += 1
            knm.append(obst.calcKLDivergence(p0, P[2+i], 10))
            km.append(obst.calcKLDivergence(p0, P[3+i], 10))
        K.append(knm)
        K.append(km)
        kc = obst.calcKLDivergence(p0, P[-1], 10)
        K.append([kc for i in rng])
    print "Saving Divergences"
    path = "./Resultados/kldivergences_"+t+".txt" 
    f = open(path, 'w')
    for kld in K:
        f.write(resultToString(kld))
    f.close()
    return K
      
    
def compareSequences(t, l, a, e, ac, k, ranges):
    print "Opening original sequence"
    if t == "henon":
        path = "../Sequencias/MH6.dat"
    elif t == "even":
        path = "./Resultados/sequence_evenshift_original_10000000.txt"
    elif t == "tri":
        path = "./Resultados/sequence_trishift_original_10000000.txt"
    s = []
    s.append(readSequenceFile(path))
    print "Opening D-Markov Sequence"
    path = "./Resultados/sequence_"+t+"generated_L_X_alpha_X_dmarkov9.txt"
    s.append(readSequenceFile(path))
    
    lrange, alpharange = ranges
    
    #Opening files first. If error occurs here, no time was wasted processing
    #what will need to be processed again once this functions is ran again
    for alpha in alpharange:
        print "Alpha:"
        print alpha
        for L in lrange:
	        print "L:"
	        print L
	        #No Moore:
	        print "Opening No Moore Sequence"
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
	        s.append(readSequenceFile(path))
            #With Moore:
	        print "Opening sequence w/ Moore"
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
	        s.append(readSequenceFile(path))
        print "Opening CRiSSiS Sequence"
        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        s.append(readSequenceFile(path))
    
    P, P_cond = computeProbabilities(t, s)
            
    if e:
        H = computeEntropies(t, P, P_cond)
        
    if ac:    
        A = computeAutocorrelation(t, s)
             
    if k:
        K = computeKLD(t, P, a, l, ranges)
    
    return
            
def main(argv):
    t, g, s, l, a, c, ac, e, k = readInput(argv)
    ranges = defineRanges(l, a)
    print c
    if g:
        generateGraphs(t, ranges)
    if s:
        generateSequences(t, ranges)
    if c:
    	compareSequences(t, l, a, e, ac, k, ranges)
    return 0

def readInput(argv):
	t = ""
	s = True
	g = True
	a = True
	l = True
	c = True
	ac = True
	e = True
	k = True
	try:
		opts, args = getopt.getopt(argv, "ht:g:s:l:a:c:i:e:k:", ["type=", "graph=", "sequence=", "L=", "alpha=", "compare=", "autocorrelation=", "entropy=", "kld="])
	except getopt.GetoptError:
		print 'test_generated_graph.py -t <type> -g <graph> -s <sequence> -l <L> -a <alpha> -c <compare> -i <autocorrelation> -e <entropy> -k <kld>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'test_generated_graph.py -t <type> -g <graph> -s <sequence> -l <L> -a <alpha> -c <compare> -i <autocorrelation> -e <entropy> -k <kld>'
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
		elif opt in ("-c", "--compare"):
		    	if arg == 'True':
			    c = True
			else:
			    c = False
		elif opt in ("-i", "--autocorrelation"):
		    	if arg == 'True':
			    ac = True
			else:
			    ac = False
		elif opt in ("-e", "--entropies"):
		    	if arg == 'True':
			    e = True
			else:
			    e = False
		elif opt in ("-k", "--kld"):
		    	if arg == 'True':
			    k = True
			else:
			    k = False
	return [t, g, s, l, a, c, ac, e, k]

if __name__ == "__main__":
	main(sys.argv[1:])
