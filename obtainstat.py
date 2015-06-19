from random import random
from numpy import log2
import matplotlib.pyplot as plt

def calcProbs(data, L):
    l = 1
    probs = []
    alphabet = []
    while l <= L:
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
    return [probs, alphabet]
    
def calcCondProbs(P, L, alphabet):
    #Initialize the conditional probabilities with the first node: probabilities
    #of occurence of the alphabet's symbols:
    P_cond = [P[0]]
    l = 0
    while l < L:
        d = {}
        l1 = P[l]
        l2 = P[l] if l == (L-1) else P[l+1]
        for s in alphabet:
            for a in l1:
                cond = s + "|" + a
                b = a if l < L else a[1:]
                t = b + s
                if t in l2.keys():
                    d[cond] = l2[t]/l1[a]
                else:
                    d[cond] = 0.0
        P_cond.append(d)
        l += 1
    return P_cond  
    
def calcCondEntropy(P, P_cond, L, alphabet):
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
    plt.show()
    return h                 
    
def evenShift(L, p00):
    count = 1
    out = []
    states = [0, 1]
    #Initialize state:
    r = random()
    state = states[0] if r < 0.5 else states[1]
    while count <= L:
        r = random()
        if state == states[0]:
            a = 0 if r < p00 else 1
            state = states[0] if r < p00 else states[1]
        else:
            a = 1
            state = states[0]
        out.append(a)
        count +=1
    return out     
