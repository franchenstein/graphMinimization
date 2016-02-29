from random import random
from numpy import log2
import matplotlib.pyplot as plt
import shifts
import multiprocessing as mp
import math

def calcProbsForOneLength(data, l, alphabet):
    d = dict()
    r = range(0, len(data) - (l - 1))
    for i in r:
        currentValue = ''.join(str(e) for e in data[i:i+l])
        if l == 1:
            if currentValue not in alphabet:
                alphabet.append(currentValue)
            if currentValue in d.keys():
                d[currentValue] += 1
            else:
                d[currentValue] = 1
    return [d, alphabet]

def calcProbs(data, L, output):
    l = 1
    probs = []
    alphabet = []
    while l <= L + 1:
        #d, alphabet = calcProbsForOneLength(data, l, alphabet)
        d = dict()
        r = range(0, len(data) - (l - 1))
        for i in r:
            currentValue = ''.join(str(e) for e in data[i:i+l])
            #Deduce alphabet:
            if l == 1:
                if not currentValue in alphabet:
                    alphabet.append(currentValue)
            #Count number of occurences of subsequence:
            if currentValue in d:
                d[currentValue] += 1
            else:
                d[currentValue] = 1
        for key in d:
            d[key] = d[key]/float(len(data))
        probs.append(d)
        l += 1
    output.put([probs, alphabet])
    return [probs, alphabet]
    
def calcProbsInParallel(data, L, numSubs, output):
    subLength = len(data)/numSubs
    lastSubLength = len(data)%numSubs
    subs = [data[i:i+subLength] for i in range(numSubs)]
    if lastSubLength > 0:
        lastSub = data[-lastSubLength:]
        subs.append(lastSub)
        numSubs += 1
    processes = [mp.Process(target = calcProbs, args = (subs[i], L, output))
                    for i in range(numSubs)]
    for p in processes:
        p.start()        
    for p in processes:
        p.join()
        
    results = [output.get() for p in processes]
    counts = [x[0] for x in results]
    countsByLength = []
    for c in counts:
	countsByLength.append(createDictsByLength(c, L))
    probs = []
    for i in range(L+1):
        p = [x[i] for x in countsByLength]
        p = mergeDicts(p)
        for key in p.keys():
            p[key] = p[key]/float(len(data))
	    probs.append(p)
     
    alphs = [x[1] for x in results]
    a = alphs[0]
    for b in alphs[1:]:
        a += b
    alphabet = list(set(a))
    
    return [probs, alphabet]
    
def mergeDicts(dicts):
    d0 = dicts[0]
    k = len(d0.keys()[0])
    for d in dicts[1:]:
	    for key in d.keys():
                if key in d0.keys():
                    d0[key] += d[key]
                else:
	                d0[key] = d[key]
    return d0   
    
def createDictsByLength(dicts, L):
    p = []
    for i in range(1,L+2):
	d = {}
	for e in dicts:
	    for k in e.keys():
		if len(k) == i:
		    if k in d.keys():
			d[k] += e[k]
		    else:
			d[k] = e[k]
	p.append(d)
    return p
    
def calcCondProbs(P, L, alphabet):
    #Initialize the conditional probabilities with the first node: probabilities
    #of occurence of the alphabet's symbols:
    P_cond = [P[0]]
    l = 0
    while l < L:
        d = {}
        l1 = P[l]
        l2 = P[l+1]
        for s in alphabet:
            for a in l1:
                cond = s + "|" + a
                t = a + s
                if t in l2.keys():
                    d[cond] = l2[t]/l1[a]
                else:
                    d[cond] = 0.0
        P_cond.append(d)
        l += 1
    return P_cond  
    
def calcCondEntropy(P, P_cond, L):
    h = []
    n = 0
    l = 0
    while l < L:
        acc = 0
        l1 = P[l]
        l2 = P_cond[l]
        for a in l1:
            if l == 0:
                acc -= l1[a]*log2(l1[a])
            else:
                s = a[-1] + "|" + a[0:-1]
                if not l2[s] == 0:
                    acc -= l1[a]*log2(l2[s])
        h.append(acc)
        l += 1
    plt.plot(h)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,0,1))
    plt.show()
    return h
    
def calcKLDivergence(P1, P2, L):
    K = []
    for i in range(0,L):
        KLD = 0
        for k in P1[i].keys():
            p = P1[i][k]
            if k in P2[i].keys():
                q = P2[i][k]
            else:
                q = 1e-15
            KLD += p*math.log(p/q,2)
        K.append(KLD)
    return K 
    
def saveAsStates(P_cond, alphabet, filePath):
    f = open(filePath, 'w') #File open as writeble.
    lines = []
    i = 0
    L = len(P_cond)
    
    for probDict in P_cond:
        ks = probDict.keys()
        if i == 0:
            lines.append("e\n")
            for k in ks:
                lines.append(k + " " + k + " " + str(probDict[k]) + "\n")
            lines.append("\n")
        else:
            names = [x[(x.index("|") + 1):] for x in ks]
            states = list(set(names))
            for state in states:
                lines.append(state + "\n")
                for a in alphabet:
                    s = str(probDict[ a + "|" + state])
                    #if float(s) > 0.0:
                    t = state if i < (L - 1) else state[1:]
                    n = t + a
                    lines.append( a + " " + n + " " + s + "\n")
                lines.append("\n")    
        i += 1
    f.writelines(lines)
    f.close()
    
def generate(shiftType, L, p):
    s = shiftType.lower()
    if s == "even":
        return shifts.evenShift(L, p)
    elif s == "bin":
        return shifts.binShift(L, p)
    elif s == "tri":
        return shifts.triShift(L, p) 
    elif s == "ternary":
        return shifts.ternaryShift(L, p)                                  
