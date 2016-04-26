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
import numpy as np
import matplotlib.pyplot as plt

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
	g.parseGraphFile("../Resultados/graph_henon_L15.txt")
	w = ["1111", "001100", "101101", "110111"] 
    elif t == "even":
	g.parseGraphFile("../Resultados/graph_evenshift_10000000_L15.txt")
	w = ["0"]
    elif t == "tri":
	g.parseGraphFile("../Resultados/graph_trishift_10000000_L15.txt")
	w = ["00"]
    elif t == "10dbq1":
        g.parseGraphFile("../Resultados/graph_10dB_0.005_q=1_L12.txt")
        w = ["11111", "01111", "010001", 
             "1100011", "1000101", "0000000",
             "1000001", "00011000"]
    elif t == "quaternary":
        g.parseGraphFile("../Resultados/graph_quaternary_L8.txt")
        w = ["3", "2", "00", 
             "01", "10", "11"]
    return [g, w]
    
def genDMarkovGraphs(t, d_ini, d_end):
    g = pg.ProbabilisticGraph([], [])
    g, w = openGraph(t, g)
    for d in range(d_ini, d_end + 1):      
        dm = dmarkov.DMarkov(g, d)
        path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
        dm.saveGraphFile(path) 
        
def genMk1Graphs(t, L_ini, L_end, alpha_ini, alpha_end, expn, mooreIters = -1):
    Lrange = range(L_ini, L_end + 2, 2)
    if alpha_ini == alpha_end:
        alpharange = [alpha_ini]
    else:
        alpharange = np.arange(alpha_ini, alpha_end + 0.05, 0.05)
    g = pg.ProbabilisticGraph([], [])
    if alpha_end == 0.99:
        np.append(alpharange, 0.99)
    for alpha in alpharange:
        for L in Lrange:
            g,w = openGraph(t, g)
            if expn == 'dmark':
                dm = dmarkov.DMarkov(g, L-1)
                ns = [x for x in g.states if x.nameLength() < L-1]
                ns.extend(dm.states)
                h = pg.ProbabilisticGraph(ns, g.alphabet)
                Q = h.createInitialPartition(h.stateNamed(w[0]), L+10, alpha, 'chi-squared')
            else:                
                if expn == 'old':
                    Q = g.createInitialPartition(g.stateNamed(w[0]), L, alpha, 'chi-squared')
                elif expn == 'new':
                    Q = g.createInitialPartition2(g.stateNamed(w[0]), L, alpha, 'chi-squared')
                shortStates = [x for x in g.states if x.nameLength() < L]
                h = pg.ProbabilisticGraph(shortStates, g.alphabet)
                h = h.removeUnreachableStates()
            P = []
            for q in Q:
                p = q.pop(0)
                p1 = pt.Partition(p)
                while q:
                    p1.addToPartition(q.pop(0))
                P.append(p1)
            PS = ps.PartitionSet(P)
            ip = gm.moore(PS, h, mooreIters)
            j = ip.recoverGraph(h)
            path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_mk1_exp_'+str(expn)
            if mooreIters > 0:
                path += '_mooreUpTo_'+str(mooreIters)+'.txt'
            else:
                path += '.txt'
            j.saveGraphFile(path)
            
def genMk2Graphs(t, L_ini, L_end, alpha_ini, alpha_end, expn):
    Lrange = range(L_ini, L_end + 2, 2)
    if alpha_ini == alpha_end:
        alpharange = [alpha_ini]
    else:
        alpharange = np.arange(alpha_ini, alpha_end + 0.05, 0.05)
    g = pg.ProbabilisticGraph([], [])
    if alpha_end == 0.99:
        np.append(alpharange, 0.99)
    g = pg.ProbabilisticGraph([], [])
    if alpha_end == 0.99:
        np.append(alpharange, 0.99)
    for L in Lrange:
        for alpha in alpharange:
            g, w = openGraph(t, g)
            if expn == 'dmark':
                dm = dmarkov.DMarkov(g, L-1)
                shortStates = [x for x in g.states if x.nameLength() < L-1]
                shortStates.extend(dm.states)
            else:
                z = [x for x in g.states if x.nameLength() == L-1]
                for s in z:
                    if expn == 'old':
                        g.expandLastLevel(s, alpha, 'chi-squared')
                    elif expn == 'new':
                        g.expandLastLevel2(s, alpha, 'chi-squared') 
                shortStates = [x for x in g.states if x.nameLength() <= L-1]
            gd = pg.ProbabilisticGraph(shortStates, g.alphabet)
            l = gm.minimizeFromSynchWords(gd, w)
            m = l.removeUnreachableStates()
            path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_mk2_exp_'+str(expn)+'.txt'
            m.saveGraphFile(path)
            
def genSequences(t, orig, alg, l, L_ini = 6, L_end = 12, 
                      alpha_ini = 0.8, alpha_end = 0.99, expn = 'dmark', 
                      mooreIters = -1):
    g = pg.ProbabilisticGraph([], [])
    if orig:
        if t == 'even' or t == 'tri':
            probfile = t+'shiftprobs.txt'
            f = open(probfile, 'r')
            probs = []
            for line in f:
                probs.append(float(line))
            f.close()
            d = obst.generate(t, l, probs)
            path = "../Resultados/sequence_"+t+"shift_original_"+str(l)+".json"
            f2 = open(path, 'w')
            json.dump(d, f2)
            f2.close()
            
    else:
        if alg == 'dmark':
            for d in range(L_ini, L_end + 1):
                path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                g.parseGraphFile(path)
                data = g.generateSequence(l, g.states[0])
                path = '../Resultados/sequence_'+t+'generated_dmarkov_'+str(d)+'.json'
                f = open(path, 'w')
                json.dump(data, f)
                f.close()
        else:
            Lrange = range(L_ini, L_end + 2, 2)
            if alpha_ini == alpha_end:
                alpharange = [alpha_ini]
            else:
                alpharange = np.arange(alpha_ini, alpha_end + 0.05, 0.05)
            g = pg.ProbabilisticGraph([], [])
            if alpha_end == 0.99:
                np.append(alpharange, 0.99)
            for alpha in alpharange:
                for L in Lrange:
                    graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)
                    if mooreIters > 0:
                        graph_path += '_mooreUpTo_'+str(mooreIters)+'.txt'
                    else:
                        graph_path += '.txt'
                    g.parseGraphFile(graph_path)
                    data = g.generateSequence(l, g.states[0])
                    sequence_path = '../Resultados/sequence_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)
                    if mooreIters > 0:
                        sequence_path += '_mooreUpTo_'+str(mooreIters)+'.json'
                    else:
                        sequence_path += '.json'    
                    f = open(sequence_path, 'w')
                    json.dump(data, f)
                    f.close()
                    
def openSequences(t, alg, orig, L_ini, L_end, alpha_ini, alpha_end, expn, mooreIters = -1):
    s = []  
    p_path = '../Resultados/probabilities_' + t + '_' + alg + '_' + expn
    pcond_path = '../Resultados/conditional_probabilities_' + t + '_' + alg + '_' + expn
    if mooreIters > 0:
        p_path += '_mooreUpTo_'+str(mooreIters)+'.json'
        pcond_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        p_path += '.json'
        pcond_path += '.json'             
    if orig:
        if t == "henon":
            path = "../../Sequencias/MH6.dat"
        elif t == "even":
            path = "../Resultados/sequence_evenshift_10000000_original.txt"
        elif t == "tri":
            path = "../Resultados/sequence_trishift_original_10000000.txt"
        elif t == "10dbq1":
            path = "../../Sequencias/seq10db_q1.txt"
        elif t == "quaternary":
            path = "../../Sequencias/quaternary_seq.txt"
        s.append(readSequenceFile(path))
            
    else:
        if alg == 'dmark':
            for d in range(L_ini, L_end + 1):
                seq_path = '../Resultados/sequence_'+t+'generated_dmarkov_'+str(d)+'.json'
                f = open(seq_path, 'r')
                s.append(json.load(f))
                f.close()
        else:
            if alg == 'dmark':
                Lrange = range(L_ini, L_end + 1)
            else:
                Lrange = range(L_ini, L_end + 2, 2)
            if alpha_ini == alpha_end:
                alpharange = [alpha_ini]
            else:
                alpharange = np.arange(alpha_ini, alpha_end + 0.05, 0.05)
            g = pg.ProbabilisticGraph([], [])
            if alpha_end == 0.99:
                np.append(alpharange, 0.99)
            for alpha in alpharange:
                for L in Lrange:
                    seq_path = '../Resultados/sequence_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)
                    if mooreIters > 0:
                        seq_path += '_mooreUpTo_'+str(mooreIters)+'.json'
                    else:
                        seq_path += '.json'  
                    f = open(seq_path, 'r')
                    s.append(json.load(f))
                    f.close()                      
    return s, p_path, pcond_path
                    
def calcProbs(t, orig, alg, l, L_ini = 6, L_end = 12, 
                      alpha_ini = 0.8, alpha_end = 0.99, expn = '', mooreIters = -1):
        s, p_path, pcond_path = openSequences(t, alg, orig, L_ini, L_end, alpha_ini, alpha_end, expn, mooreIters)
        if not os.path.isfile(p_path):
            P, P_cond = calcProbsFromSeqs(s, l)
            f = open(p_path, 'w')
            json.dump(P,f)
            f.close()
            f = open(pcond_path, 'w')
            json.dump(P_cond,f)
            f.close()           
        
def calcProbsFromSeqs(s, L):
    P = []
    Alph = []
    P_cond = []
    q = mp.Queue()
    for seq in s:
        p, alph = obst.calcProbs(seq, L, q)
        P.append(p)
        Alph.append(alph)
        pcond = obst.calcCondProbs(p, L, alph)
        P_cond.append(pcond)
    return P, P_cond     
    
def calcEntropies(t, alg, L, expn, mooreIters = -1):
    H = []  
    p_path = '../Resultados/probabilities_' + t + '_' + alg + '_' + expn
    pcond_path = '../Resultados/conditional_probabilities_' + t + '_' + alg + '_' + expn
    if mooreIters > 0:
        p_path += '_mooreUpTo_'+str(mooreIters)+'.json'
        pcond_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        p_path += '.json'
        pcond_path += '.json' 
    f = open(p_path, 'r')
    P = json.load(f)
    f.close()
    f = open(pcond_path, 'r')
    P_cond = json.load(f)
    f.close()
    i = 0
    for p in P:
        h = obst.calcCondEntropy(p, P_cond[i], L)
        i += 1
        H.append(h)
    h_path = '../Resultados/entropies_'+t+'_'+alg+'_' + expn
    if mooreIters > 0:
        h_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        h_path += '.json' 
    f = open(h_path, 'w')
    json.dump(H, f)
    f.close()     
    
def calcKLD(t, alg, L, expn = '', mooreIters = -1):
    K = []  
    orig_path = '../Resultados/probabilities_' + t + '_original_.json'
    f = open(orig_path, 'r')
    Porig = json.load(f)
    f.close()
    p_path = '../Resultados/probabilities_' + t + '_' + alg + '_' + expn
    if mooreIters > 0:
        p_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        p_path += '.json' 
    f = open(p_path, 'r')
    P = json.load(f)
    f.close()
    
    p0 = Porig[0]
                
    for p in P:
        k = obst.calcKLDivergence(p0, p, L)
        K.append(k)
    k_path = '../Resultados/kldivergences_'+t+'_'+alg+'_' + expn
    if mooreIters > 0:
        k_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        k_path += '.json' 
    f = open(k_path, 'w')
    json.dump(K, f)
    f.close() 
    
def calc_l1_metric(t, alg, N, expn = '', mooreIters = -1):
    L1 = []  
    orig_path = '../Resultados/probabilities_' + t + '_original_.json'
    f = open(orig_path, 'r')
    Porig = json.load(f)
    f.close()
    p_path = '../Resultados/probabilities_' + t + '_' + alg + '_' + expn
    if mooreIters > 0:
        p_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        p_path += '.json' 
    f = open(p_path, 'r')
    P = json.load(f)
    f.close()
    
    p0 = Porig[0]
                
    for p in P:
        l1 = obst.l1Metric(p0, p, N-1)
        L1.append(l1)
    l_path = '../Resultados/l1metric_'+t+'_'+alg+'_' + expn
    if mooreIters > 0:
        l_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        l_path += '.json' 
    f = open(l_path, 'w')
    json.dump(L1, f)
    f.close()

def calc_kld_metric(t, alg, N, expn = '', mooreIters = -1):
    KM = []  
    orig_path = '../Resultados/probabilities_' + t + '_original_.json'
    f = open(orig_path, 'r')
    Porig = json.load(f)
    f.close()
    p_path = '../Resultados/probabilities_' + t + '_' + alg + '_' + expn 
    if mooreIters > 0:
        p_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        p_path += '.json' 
    f = open(p_path, 'r')
    P = json.load(f)
    f.close()
    
    p0 = Porig[0]
                
    for p in P:
        km = obst.l1Metric(p0, p, N-1)
        KM.append(km)
    km_path = '../Resultados/kldmetric_'+t+'_'+alg+'_' + expn
    if mooreIters > 0:
        km_path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        km_path += '.json' 
    f = open(km_path, 'w')
    json.dump(KM, f)
    f.close()
    
def calcAutoCorr(t, alg, L, orig, L_ini, L_end, alpha_ini, alpha_end, expn, mooreIters = -1):
    s, dum, mud = openSequences(t, alg, orig, L_ini, L_end, alpha_ini, alpha_end, expn, mooreIters)
    A = []
    for seq in s:
        a = obst.autocorrelation(seq,L)
        A.append(a)
    print "Saving Autocorrelations"
    path = "../Resultados/autocorrelations_"+t+"_"+alg+"_" + expn 
    if mooreIters > 0:
        path += '_mooreUpTo_'+str(mooreIters)+'.json'
    else:
        path += '.json' 
    f = open(path, 'w')
    json.dump(A, f)
    f.close()
    return A
    
def plotEntropies(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, D_ini, D_fin):
    labels = []
    line = ['']
    H = []
    Ho_path = '../Resultados/entropies_'+t+'_original_.json'
    g = pg.ProbabilisticGraph([], [])
    f = open(Ho_path, 'r')
    original = json.load(f)
    for h in original:
        H.append(h)
    labels.append("Original Sequence")
    f.close()
    algs = []
    expn = []
    m = False
    if dmark['Enable'] == True:
        algs.append('dmark')
    if mk1['Enable'] == True:
        algs.append('mk1')
        if mk1['moore'] == True:
            m = True
            Mi = mk1['ini']
            Mf = mk1['end']
    if mk2['Enable'] == True:
        algs.append('mk2')
    for alg in algs:
        hpaths = []
        if alg == 'dmark':
            #Path:
            hpath = '../Resultados/entropies_'+t+'_'+alg+'_.json'
            hpaths.append(hpath)
            #Labels:
            for d in range(D_ini, D_fin + 1):
                path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                g.parseGraphFile(path)
                l = len(g.states)
                lb = str(d) + '-Markov, ' + str(l) + ' states'
                labels.append(lb)
                line.append('')
        else:
            #Path:
            if alg == 'mk1':
                opts = mk1
            else:
                opts = mk2
            expns = []
            for k in opts.keys():
                if k != 'Enable':
                    if opts[k]:
                        expns.append(k) 
                        hpath = '../Resultados/entropies_'+t+'_'+alg+'_'+k+'.json'
                        hpaths.append(hpath)
            #Labels:
            Lrange = range(L_ini, L_fin + 2, 2)
            if alpha_ini == alpha_fin:
                alpharange = [alpha_ini]
            else:
                alpharange = np.arange(alpha_ini, alpha_fin + 0.05, 0.05)
            g = pg.ProbabilisticGraph([], [])
            if alpha_fin == 0.99:
                np.append(alpharange, 0.99)
            for alpha in alpharange:
                for L in Lrange:
                    for expn in expns:
                        graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'.txt'
                        g.parseGraphFile(graph_path)
                        l = len(g.states)
                        lb = alg + ", L = " + str(L) + ", alpha = " + str(alpha) + ", " + expn + " expansion, " + str(l) + " states"
                        labels.append(lb)
                        if alg == 'mk1':
                            line.append('--')
                        else:
                            line.append('o')                    
           
        for hpath in hpaths:     
            f = open(hpath, 'r')
            entrops = json.load(f)
            for h in entrops:
                H.append(h)
            f.close()
            
     
    i = 0 
    x = range(0, len(H[0]))          
    for h in H:
        if i == 0:
            plt.plot(x, h, 'k', linewidth = 3, label = labels[i])
        else:
            plt.plot(x, h, line[i], label = labels[i])               
        i+=1
    
    legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
    plt.show()  
    
def plotEntropiesByNoStates(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, D_ini, D_fin, final):
    H = []
    labels = []
    Ho_path = '../Resultados/entropies_'+t+'_original_.json'
    g = pg.ProbabilisticGraph([], [])
    f = open(Ho_path, 'r')
    original = json.load(f)
    for h in original:
        Hbase = h[final]
    f.close()
    algs = []
    expn = []
    m = False
    if dmark['Enable'] == True:
        algs.append('dmark')
    if mk1['Enable'] == True:
        algs.append('mk1')
        if mk1['moore'] == True:
            m = True
            Mi = mk1['ini']
            Mf = mk1['end']
    if mk2['Enable'] == True:
        algs.append('mk2')
    xranges = []
    for alg in algs:
        hpaths = []
        if alg == 'dmark':
            #Path:
            hpath = '../Resultados/entropies_'+t+'_'+alg+'_.json'
            hpaths.append(hpath)
            x =[]
            for d in range(D_ini, D_fin + 1):
                path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                g.parseGraphFile(path)
                l = len(g.states)
                x.append(l)
            #Labels:
            labels.append('D-Markov')
            xranges.append(x)
        else:
            #Path:
            if alg == 'mk1':
                opts = mk1
            else:
                opts = mk2
            expns = []
            for k in opts.keys():
                if k != 'Enable' and k != 'moore' and k != 'ini' and k != 'end':
                    if opts[k]:
                        expns.append(k) 
                        if m:
                            mrange = range(Mi, Mf+1)
                            for M in mrange:
                                hpath = '../Resultados/entropies_'+t+'_'+alg+'_'+k+'_mooreUpTo_'+str(M)+'.json'
                                hpaths.append(hpath)                                
                        else:
                            hpath = '../Resultados/entropies_'+t+'_'+alg+'_'+k+'.json'
                            hpaths.append(hpath)
            #Labels:
            Lrange = range(L_ini, L_fin + 2, 2)
            if alpha_ini == alpha_fin:
                alpharange = [alpha_ini]
            else:
                alpharange = np.arange(alpha_ini, alpha_fin + 0.05, 0.05)
            g = pg.ProbabilisticGraph([], [])
            if alpha_fin == 0.99:
                np.append(alpharange, 0.99)
            for expn in expns:
                if m:
                    mrange = range(Mi, Mf + 1)
                else:
                    mrange = [-1]
                for M in mrange:
                    x = []
                    for alpha in alpharange:
                        for L in Lrange:
                            if m:
                                graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'_mooreUpTo_'+str(M)+'.txt'
                            else:
                                graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'.txt'
                            g.parseGraphFile(graph_path)
                            l = len(g.states)
                            x.append(l)
                    if m:
                        lb = alg + ", " + expn + ', Moore up to ' + str(M)
                    else:
                        lb = alg + ", " + expn
                    labels.append(lb)
                    xranges.append(x)                   
           
        for hpath in hpaths:     
            f = open(hpath, 'r')
            entrops = json.load(f)
            h = [z[final] for z in entrops]
            H.append(h)
            f.close()
            
     
    i = 0         
    for h in H:
        plt.semilogx(xranges[i], h, marker = 'o', label = labels[i])               
        i+=1
    
    plt.axhline(y = Hbase, color = 'k', linewidth = 3, label = 'Original Sequence Baseline')
    legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
    plt.show()  

def plotKLD(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, D_ini, D_fin, byNoStates):
    labels = []
    g = pg.ProbabilisticGraph([],[])
    K = []
    algs = []
    expn = []
    ranges = []
    m = False
    if dmark['Enable'] == True:
        algs.append('dmark')
    if mk1['Enable'] == True:
        algs.append('mk1')
        if mk1['moore'] == True:
            m = True
            Mi = mk1['ini']
            Mf = mk1['end']
    if mk2['Enable'] == True:
        algs.append('mk2')
    for alg in algs:
        kpaths = []
        if alg == 'dmark':
            #Path:
            kpath = '../Resultados/kldivergences_'+t+'_'+alg+'_.json'
            kpaths.append(kpath)
            if byNoStates:            
                x = []
                for d in range(D_ini, D_fin + 1):
                    path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                    g.parseGraphFile(path)
                    l = len(g.states)
                    x.append(l)
                ranges.append(x)
            else:
                ranges.append(range(D_ini, D_fin + 1))
            labels.append("Original Sequence vs. D-Markov")
        else:
            #Path:
            if alg == 'mk1':
                opts = mk1
            else:
                opts = mk2
            expns = []
            for k in opts.keys():
                if k != 'Enable' and k != 'moore' and k != 'ini' and k != 'end':
                    if opts[k]:
                        expns.append(k) 
                        if m:
                            mrange = range(Mi, Mf + 1)
                            for M in mrange:
                                kpath = '../Resultados/kldivergences_'+t+'_'+alg+'_'+k+'_mooreUpTo_'+str(M)+'.json'
                                kpaths.append(kpath)
                        else:
                            kpath = '../Resultados/kldivergences_'+t+'_'+alg+'_'+k+'.json'
                            kpaths.append(kpath)
                        #Labels:
                        if byNoStates:
                            Lrange = range(L_ini, L_fin + 2, 2)
                            if alpha_ini == alpha_fin:
                                alpharange = [alpha_ini]
                            else:
                                alpharange = np.arange(alpha_ini, alpha_fin + 0.05, 0.05)
                            g = pg.ProbabilisticGraph([], [])
                            if alpha_fin == 0.99:
                                np.append(alpharange, 0.99)
                            for expn in expns:
                                if m:
                                    mrange = range(Mi, Mf + 1)
                                else:
                                    mrange = [-1]
                                for M in mrange:
                                    x = []
                                    for alpha in alpharange:
                                        for L in Lrange:
                                            if m:
                                                graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'_mooreUpTo_'+str(M)+'.txt'
                                            else:
                                                graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'.txt'
                                            g.parseGraphFile(graph_path)
                                            l = len(g.states)
                                            x.append(l)
                                    ranges.append(x)
                        else:
                            ranges.append(range(L_ini, L_fin + 2, 2))
                        if m:
                            for M in mrange:
                                lb = "Original Sequence vs. " + alg + " " + k + "expansion, Moore up to " + str(M)
                                labels.append(lb)
                        else:
                            lb = "Original Sequence vs. " + alg + " " + k + "expansion"
                            labels.append(lb)             
           
        for kpath in kpaths:     
            f = open(kpath, 'r')
            divs = json.load(f)
            K.append(divs)
            f.close()
            
    i = 0       
    for k in K:
        plt.semilogx(ranges[i], k, marker = 'o', label = labels[i])
        i += 1
    
    legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
    plt.show()

def plotL1Metric(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, D_ini, D_fin, byNoStates):
    labels = []
    g = pg.ProbabilisticGraph([],[])
    K = []
    algs = []
    expn = []
    ranges = []
    m = False
    if dmark['Enable'] == True:
        algs.append('dmark')
    if mk1['Enable'] == True:
        algs.append('mk1')
        if mk1['moore'] == True:
            m = True
            Mi = mk1['ini']
            Mf = mk1['end']
    if mk2['Enable'] == True:
        algs.append('mk2')
    for alg in algs:
        kpaths = []
        if alg == 'dmark':
            #Path:
            kpath = '../Resultados/l1metric_'+t+'_'+alg+'_.json'
            kpaths.append(kpath)
            if byNoStates:            
                x = []
                for d in range(D_ini, D_fin + 1):
                    path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                    g.parseGraphFile(path)
                    l = len(g.states)
                    x.append(l)
                ranges.append(x)
            else:
                ranges.append(range(D_ini, D_fin + 1))
            labels.append("Original Sequence vs. D-Markov")
        else:
            #Path:
            if alg == 'mk1':
                opts = mk1
            else:
                opts = mk2
            expns = []
            for k in opts.keys():
                if k != 'Enable' and k != 'moore' and k != 'ini' and k != 'end':
                    if opts[k]:
                        expns.append(k) 
                        if m:
                            mrange = range(Mi, Mf + 1)
                            for M in mrange:
                                kpath = '../Resultados/l1metric_'+t+'_'+alg+'_'+k+'_mooreUpTo_'+str(M)+'.json'
                                kpaths.append(kpath)
                        else:
                            kpath = '../Resultados/l1metric_'+t+'_'+alg+'_'+k+'.json'
                            kpaths.append(kpath)
                        #Labels:
                        if byNoStates:
                            Lrange = range(L_ini, L_fin + 2, 2)
                            if alpha_ini == alpha_fin:
                                alpharange = [alpha_ini]
                            else:
                                alpharange = np.arange(alpha_ini, alpha_fin + 0.05, 0.05)
                            g = pg.ProbabilisticGraph([], [])
                            if alpha_fin == 0.99:
                                np.append(alpharange, 0.99)
                            for expn in expns:
                                if m:
                                    mrange = range(Mi, Mf + 1)
                                else:
                                    mrange = [-1]
                                for M in mrange:
                                    x = []
                                    for alpha in alpharange:
                                        for L in Lrange:
                                            if m:
                                                graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'_mooreUpTo_'+str(M)+'.txt'
                                            else:
                                                graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'.txt'
                                            g.parseGraphFile(graph_path)
                                            l = len(g.states)
                                            x.append(l)
                                    ranges.append(x)
                        else:
                            ranges.append(range(L_ini, L_fin + 2, 2))
                        if m:
                            for M in mrange:
                                lb = "Original Sequence vs. " + alg + " " + k + "expansion, Moore up to " + str(M)
                                labels.append(lb)
                        else:
                            lb = "Original Sequence vs. " + alg + " " + k + "expansion"
                            labels.append(lb)                 
           
        for kpath in kpaths:     
            f = open(kpath, 'r')
            divs = json.load(f)
            K.append(divs)
            f.close()
            
    i = 0       
    for k in K:
        plt.semilogx(ranges[i], k, marker = 'o', label = labels[i])
        i += 1
    
    legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
    plt.show()
    
def plotKLDMetric(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, D_ini, D_fin, byNoStates):
    labels = []
    g = pg.ProbabilisticGraph([],[])
    K = []
    algs = []
    expn = []
    ranges = []
    if dmark['Enable'] == True:
        algs.append('dmark')
    if mk1['Enable'] == True:
        algs.append('mk1')
    if mk2['Enable'] == True:
        algs.append('mk2')
    for alg in algs:
        kpaths = []
        if alg == 'dmark':
            #Path:
            kpath = '../Resultados/kldmetric_'+t+'_'+alg+'_.json'
            kpaths.append(kpath)
            if byNoStates:            
                x = []
                for d in range(D_ini, D_fin + 1):
                    path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                    g.parseGraphFile(path)
                    l = len(g.states)
                    x.append(l)
                ranges.append(x)
            else:
                ranges.append(range(D_ini, D_fin + 1))
            labels.append("Original Sequence vs. D-Markov")
        else:
            #Path:
            if alg == 'mk1':
                opts = mk1
            else:
                opts = mk2
            expns = []
            for k in opts.keys():
                if k != 'Enable':
                    if opts[k]:
                        expns.append(k) 
                        kpath = '../Resultados/kldmetric_'+t+'_'+alg+'_'+k+'.json'
                        kpaths.append(kpath)
                        #Labels:
                        if byNoStates:
                            Lrange = range(L_ini, L_fin + 2, 2)
                            if alpha_ini == alpha_fin:
                                alpharange = [alpha_ini]
                            else:
                                alpharange = np.arange(alpha_ini, alpha_fin + 0.05, 0.05)
                            g = pg.ProbabilisticGraph([], [])
                            if alpha_fin == 0.99:
                                np.append(alpharange, 0.99)
                            for expn in expns:
                                x =[]
                                for alpha in alpharange:
                                    for L in Lrange:
                                        graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'.txt'
                                        g.parseGraphFile(graph_path)
                                        l = len(g.states)
                                        x.append(l)
                                ranges.append(x)
                        else:
                            ranges.append(range(L_ini, L_fin + 2, 2))
                        lb = "Original Sequence vs. " + alg + " " + k + "expansion"
                        labels.append(lb)                 
           
        for kpath in kpaths:     
            f = open(kpath, 'r')
            divs = json.load(f)
            K.append(divs)
            f.close()
            
    i = 0       
    for k in K:
        plt.semilogx(ranges[i], k, marker = 'o', label = labels[i])
        i += 1
    
    legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
    plt.show()    

    
def plotAutocorr(t, dmark, mk1, mk2, L_ini, L_fin, alpha_ini, alpha_fin, D_ini, D_fin):
    labels = []
    A = []
    lines = ['']
    Ao_path = '../Resultados/autocorrelations_'+t+'_orig_.json'
    g = pg.ProbabilisticGraph([], [])
    f = open(Ao_path, 'r')
    original = json.load(f)
    for a in original:
        A.append(a)
    labels.append("Original Sequence")
    f.close()
    algs = []
    expn = []
    if dmark['Enable'] == True:
        algs.append('dmark')
    if mk1['Enable'] == True:
        algs.append('mk1')
    if mk2['Enable'] == True:
        algs.append('mk2')
    for alg in algs:
        apaths = []
        if alg == 'dmark':
            #Path:
            apath = '../Resultados/autocorrelations_'+t+'_'+alg+'_.json'
            apaths.append(apath)
            #Labels:
            for d in range(D_ini, D_fin + 1):
                path = '../Resultados/graph_'+t+'_dmarkov_'+str(d)+'.txt'
                g.parseGraphFile(path)
                l = len(g.states)
                lb = str(d) + '-Markov, ' + str(l) + ' states'
                labels.append(lb)
                lines.append('')
        else:
            #Path:
            if alg == 'mk1':
                opts = mk1
            else:
                opts = mk2
            expns = []
            for k in opts.keys():
                if k != 'Enable':
                    if opts[k]:
                        expns.append(k) 
                        apath = '../Resultados/autocorrelations_'+t+'_'+alg+'_'+k+'.json'
                        apaths.append(apath)
            #Labels:
            Lrange = range(L_ini, L_fin + 2, 2)
            if alpha_ini == alpha_fin:
                alpharange = [alpha_ini]
            else:
                alpharange = np.arange(alpha_ini, alpha_fin + 0.05, 0.05)
            g = pg.ProbabilisticGraph([], [])
            if alpha_fin == 0.99:
                np.append(alpharange, 0.99)
            for alpha in alpharange:
                for L in Lrange:
                    for expn in expns:
                        graph_path = '../Resultados/graph_'+t+'_generated_L_'+str(L)+'_alpha_'+str(alpha)+'_'+alg+'_exp_'+str(expn)+'.txt'
                        g.parseGraphFile(graph_path)
                        l = len(g.states)
                        lb = alg + ", L = " + str(L) + ", alpha = " + str(alpha) + ", " + expn + " expansion, " + str(l) + " states"
                        labels.append(lb)   
                        if alg == 'mk1':
                            lines.append('--')
                        else:
                            lines.append('o')                   
           
        for apath in apaths:     
            f = open(apath, 'r')
            entrops = json.load(f)
            for a in entrops:
                A.append(a)
            f.close()
            
     
    i = 0 
    x = range(1, len(A[0]))          
    for a in A:
        if i == 0:
            plt.plot(x, a[1:], 'k', linewidth = 3, label = labels[i])
        else:
            plt.plot(x, a[1:], lines[i], label = labels[i])
        i += 1
    
    legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
    plt.show()

#Main functions:
def generateGraphs(t, d, ranges):
    g = pg.ProbabilisticGraph([],[])
    print "Opening original tree\n"
    g, w = openGraph(t, g) 
    
    #D-Markov:
    print "Creating D-Markov Graph\n"
    if d:
        genDMarkovGraphs(t, 4, 10)
    else:    
        genDMarkovGraphs(t, 4, 4)  
        
    lrange, alpharange = ranges
    
    print "Creating partitions\n"
    for alpha in alpharange:
    	print "alpha:"
    	print alpha
    	for L in lrange:
    	    print "L:"
    	    print L
            g, w = openGraph(t, g)
            Q = g.createInitialPartition(g.stateNamed(w[0]), L, alpha, "chi-squared")
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
            #path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
            #h.saveGraphFile(path)
            
            #With Moore sequence and graph:
            print "Generating graphs after Moore\n"
            i = g.removeUnreachableStates()
            shortStates = [x for x in i.states if len(x.name) < L]
            i = pg.ProbabilisticGraph(shortStates, i.alphabet)
            ip = gm.moore(PS, i)
            j = ip.recoverGraph(i)
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
            j.saveGraphFile(path)
            
            #New Expansion Using Moore:
            g, w = openGraph(t, g)
            Q = g.createInitialPartition2(g.stateNamed(w[0]), L, alpha, "chi-squared")
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
            #path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
            #h.saveGraphFile(path)
            
            #With Moore sequence and graph:
            print "Generating graphs after Moore\n"
            i = g.removeUnreachableStates()
            shortStates = [x for x in i.states if len(x.name) < L]
            i = pg.ProbabilisticGraph(shortStates, i.alphabet)
            ip = gm.moore(PS, i)
            j = ip.recoverGraph(i)
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_exp2.txt"
            j.saveGraphFile(path)
            
            #New algorithm, ending with D-Markov:
            g, w = openGraph(t, g)
            dm = dmarkov.DMarkov(g, L)
            z = [x for x in g.states if x.nameLength() < L]
            z.extend(dm.states)
            gd = pg.ProbabilisticGraph(z, g.alphabet)
            synchlist = w
            k = gm.minimizeFromSynchWords(gd, synchlist)
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"newDMarkov.txt"
            k.saveGraphFile(path)
            #New algorithm, ending ell:
            g, w = openGraph(t, g)
            z = [x for x in g.states if x.nameLength() == L]
            for s in z:
                g.expandLastLevel(s, alpha, 'chi-squared')
            g.states = [x for x in g.states if x.nameLength() <= L]
            synchlist = w
            l = gm.minimizeFromSynchWords(g, synchlist)
            m = l.removeUnreachableStates()
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"newLastLevel.txt"
            m.saveGraphFile(path)
            #New algorithm, ending ell2:
            g, w = openGraph(t, g)
            z = [x for x in g.states if x.nameLength() == L]
            for s in z:
                g.expandLastLevel2(s, alpha, 'chi-squared')
            g.states = [x for x in g.states if x.nameLength() <= L]
            synchlist = w
            l = gm.minimizeFromSynchWords(g, synchlist)
            m = l.removeUnreachableStates()
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"newLastLevel2.txt"
            m.saveGraphFile(path)
        #CRiSSiS:
	print "Generating CRiSSiS graph\n"
        c = cr.crissis(w[0], g, alpha, "chi-squared")
        path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        c.saveGraphFile(path)
    return
    
def generateSequences(t, d, ranges):
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
        path = "./Resultados/sequence_evenshift_10000000_original.txt"
        f = open(path, 'w')
        f.write(d)
        f.close()
    elif t == "10dbq1":
        wsyn = "11111"
    elif t == "quaternary":
        wsyn = "3"
    
    lrange, alpharange = ranges
    
    print "Generating D-Markov Sequence"
    #D-Markov:  
    if d:
        for i in range(4, 11):
            path = "./Resultados/graph_"+t+"_dmarkov_"+str(i)+".txt"
            g.parseGraphFile(path)
            dmarkov = '_dmarkov' + str(i)
            generateAndSaveSequences(g, g.states[0], t, 'X', 10000000, 'X', dmarkov)
    else:  
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
	    #print "Generating NoMoore Sequence"
        #    path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
        #    g.parseGraphFile(path)
        #    generateAndSaveSequences(g, g.stateNamed(wsyn), t, L, 10000000, alpha, '_NoMoore')
            #With Moore:
            print "Generating Sequence W/ Moore"
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.states[0], t, L, 10000000, alpha, '')
            print "Generating Sequence W/ Moore new expansions"
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_exp2.txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.states[0], t, L, 10000000, alpha, 'exp2')
            print "Generating Sequence W/ New Algorithm"
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"newDMarkov.txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.states[0], t, L, 10000000, alpha, 'newDMarkov')
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"newLastLevel.txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.states[0], t, L, 10000000, alpha, 'newLastLevel')
            path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"newLastLevel2.txt"
            g.parseGraphFile(path)
            generateAndSaveSequences(g, g.states[0], t, L, 10000000, alpha, 'newLastLevel2')
	print "Generating CRiSSiS Sequence"
        path = "./Resultados/graph_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_crissis.txt"
        g.parseGraphFile(path)
        generateAndSaveSequences(g, g.states[0], t, L, 10000000, alpha, '_crissis')    
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
            P_cond.append(pcond)
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
    
def computeKLD(t, P, a, l, d, ranges):
    print "Calculating Divergences"
    K = []
    lrange, alpharange = ranges
    #D-Markov KLD:
    c = 1
    k = []
    if d:
        for j in range(1,8):
            p0 = P[0]
            pd = P[j]
            c += 1
            k.append(obst.calcKLDivergence(p0, pd, 10))
    else:
        p0 = P[0]
        pd = P[1]
        k.append(obst.calcKLDivergence(p0, pd, 10))
    if a:
        rng = range(0, len(alpharange))
        for x in k:
            K.append([x for i in rng])
        knm = []
        km = []
        kc = []
        j = 1
        for i in rng:
            print j
            j += 1
            knm.append(obst.calcKLDivergence(p0, P[1+c+i], 10))
            km.append(obst.calcKLDivergence(p0, P[2+c+i], 10))
            kc.append(obst.calcKLDivergence(p0, P[3+c+i], 10))
        K.append(knm)
        K.append(km)
        K.append(kc)
    if l:
        rng = range(0, len(lrange))
        for x in k:
            K.append([x for i in rng])
        knm = []
        km = []
        j = 1
        for i in rng:
            print j
            j += 1
            knm.append(obst.calcKLDivergence(p0, P[1+c+i], 10))
            km.append(obst.calcKLDivergence(p0, P[2+c+i], 10))
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
      
    
def compareSequences(t, l, a, e, ac, k, d, ranges):
    print "Opening original sequence"
    if t == "henon":
        path = "../Sequencias/MH6.dat"
    elif t == "even":
        path = "./Resultados/sequence_evenshift_10000000_original.txt"
    elif t == "tri":
        path = "./Resultados/sequence_trishift_original_10000000.txt"
    elif t == "10dbq1":
        path = "../Sequencias/seq10db_q1.txt"
    elif t == "quaternary":
        path = "../Sequencia/quaternary_seq.txt"
    s = []
    s.append(readSequenceFile(path))
    if d:
        for i in range(4,11):
            print i
            print "Opening D-Markov Sequence"
            path = "./Resultados/sequence_"+t+"generated_L_X_alpha_X_dmarkov"+str(i)+".txt"
            s.append(readSequenceFile(path))
    else:
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
	        #print "Opening No Moore Sequence"
	        #path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"_NoMoore.txt"
	        #s.append(readSequenceFile(path))
            #With Moore:
	        print "Opening sequence w/ Moore"
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+".txt"
	        s.append(readSequenceFile(path))
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"exp2.txt"
	        s.append(readSequenceFile(path))
	        print "Opening sequence w/ New Algorithm"
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"newDMarkov.txt"
	        s.append(readSequenceFile(path))
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"newLastLevel.txt"
	        s.append(readSequenceFile(path))
	        path = "./Resultados/sequence_"+t+"generated_L_"+str(L)+"_alpha_"+str(alpha)+"newLastLevel2.txt"
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
        K = computeKLD(t, P, a, l, d, ranges)
    
    return
            
def main(argv):
    t, g, s, l, a, c, ac, e, k, d = readInput(argv)
    ranges = defineRanges(l, a)
    print c
    if g:
        generateGraphs(t, d, ranges)
    if s:
        generateSequences(t, d, ranges)
    if c:
    	compareSequences(t, l, a, e, ac, k, d, ranges)
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
	d = True
	try:
		opts, args = getopt.getopt(argv, "ht:g:s:l:a:c:i:e:k:d:", ["type=", "graph=", "sequence=", "L=", "alpha=", "compare=", "autocorrelation=", "entropy=", "kld=", "dmarkov="])
	except getopt.GetoptError:
		print 'test_generated_graph.py -t <type> -g <graph> -s <sequence> -l <L> -a <alpha> -c <compare> -i <autocorrelation> -e <entropy> -k <kld> -d <dmarkov>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'test_generated_graph.py -t <type> -g <graph> -s <sequence> -l <L> -a <alpha> -c <compare> -i <autocorrelation> -e <entropy> -k <kld> -d <dmarkov>'
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
		elif opt in ("-d", "--dmarkov"):
		    	if arg == 'True':
			    d = True
			else:
			    d = False
	return [t, g, s, l, a, c, ac, e, k, d]

if __name__ == "__main__":
	main(sys.argv[1:])
