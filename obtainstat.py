from random import random
from numpy import log2
import matplotlib.pyplot as plt
import shifts

def calcProbs(data, L):
    l = 1
    probs = []
    alphabet = []
    while l <= L + 1:
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
    plt.show()
    return h     
    
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
                    if float(s) > 0.0:
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