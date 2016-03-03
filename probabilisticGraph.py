import graph
import obtainstat
import probabilisticState
from scipy import stats
from random import random as rd

class ProbabilisticGraph(graph.Graph):
    def __init__(self, states, alphabet):
        graph.Graph.__init__(self, states, alphabet)
        
    def compareMorphs(self, edgesA, edgesB, alpha, test):
        morphA = [float(x[2]) for x in edgesA]
        morphB = []
        #Loop to guarantee the probability distributions are in the same order:
        for a in [x[0] for x in edgesA]:
            for x in edgesB:
                if x[0] == a:
                    morphB.append(float(x[2])) 
        if morphA == morphB:
            return [True, 1.0]
        else: 
            if test == "chi-squared":
                [X, p] = stats.chisquare(morphA, morphB)         
            elif test == "ks":
                [KS, p] = stats.ks_2samp(morphA, morphB)
            return [p >= alpha, p]         

    def expandLastLevel(self, s, alpha, test):
        oe = []
    	for a in self.alphabet:
   			string = s.name + a
   			v = self.stateNamed(string)
   			if v == None:
   			    oe.append((a, string, 0.0))
   			else:
   			    l = len(string)
   			    w = []
   			    for i in range(1,l+1):
   			        if i < l:
   			            t = self.stateNamed(string[i:])
   			        else:
   			            t = self.root()
   			        if t != None:
   			            r = self.compareMorphs(v.outedges, t.outedges, alpha, test)
   			        else:
   			            r = [False, 0.0]
   			        w.append(r[1])  
   			    arg = w.index(max(w)) + 1
   			    if arg == len(w):
   			        d = self.root()
   			        d = d.name
   			    else:
   			        d = string[arg:]
   			    for e in s.outedges:
   			        if e[0] == a:
   			            oe.append((a, d, e[2]))
        s.outedges = oe
        
    def createInitialPartition(self, wsyn, L, alpha, test):
        O = []
        O.extend(self.expand(wsyn))
        P0 = [wsyn]
        P = [P0]
        while True:
            if O:
                o = O.pop(0)
                flag = False
                for p in P:
                    r = self.compareMorphs(p[0].outedges, o.outedges, alpha, test)
                    if r[0]:
                        p.append(o)
                        flag = True
                        break
                if not flag:
                    P1 = [o]
                    P.append(P1)
                if len(o.name) == (L - 1):
                    self.expandLastLevel(o, alpha, test)
                a = self.expand(o)
                n = []
                for p in P:
                    for q in p:
                        n.append(q.name)
                n = list(set(n))
                a = [x for x in a if x.name not in n]
                O.extend(a)
            else:
                return P
                
    def generateSequence(self, length, iniState):
        data = ""
        s = iniState
        for i in range(0,length):
            dist = [0]
            d = [float(x[2]) for x in s.outedges]
            dist.extend(d)
            r = rd()
            c = 0
            for j in range(0,len(dist)-1):
                c += dist[j]
                if (c <= r < c + dist[j+1]):
                    a = s.outedges[j]
                    data += a[0]
                    w = s.nextStateFromEdge(a[0])
                    s = self.stateNamed(w)
                    break
        return data
                
