#!/usr/bin/env
import obtainstat as os
import matplotlib as plt
import multiprocessing as mp
import numpy as np

q = mp.Queue()

so = os.generate("tri", 10000000, [0.5, 0.8, 0.7])

L = 15
Po, alpho = os.calcProbs(so, L, q)
Pcondo = os.calcCondProbs(Po, L, alpho)
Ho = os.calcCondEntropy(Po, Pcondo, L)

f1 = "./Resultados/sequence_trishift_generated_L"
f2 = "_10000000.txt"
f2nm = "_10000000_NoMoore.txt"

s = []
for i in range(4,12,2):
    f = f1+str(i)+f2
    fi = open(f)
    s.append(list(fi.read()))
    fi.close()
    
for x in s:
    for i in range(0,len(x)):
        x[i] = int(x[i])

P = []
Pcond = []
H = []
for x in s:
    p, alph = os.calcProbs(x, L, q)
    P.append(p) 
    pcond = os.calcCondProbs(p, L, alph)
    Pcond.append(pcond)
    h = os.calcCondEntropy(p, pcond, L)
    H.append(h)
    
KL = []
for x in P:
    kl =  os.calcKLDivergence(Po, x, 10)
    KL.append(kl)

snm = []
for i in range(4,12,2):
    f = f1+str(i)+f2nm
    fi = open(f)
    snm.append(list(fi.read()))
    fi.close()
    
for x in snm:
    for i in range(0,len(x)):
        x[i] = int(x[i])

Pnm = []
Pcond_nm = []
Hnm = []
for x in snm:
    p, alph = os.calcProbs(x, L, q)
    Pnm.append(p) 
    pcond = os.calcCondProbs(p, L, alph)
    Pcond_nm.append(pcond)
    h = os.calcCondEntropy(p, pcond, L)
    Hnm.append(h)
    
KLnm = []
for x in Pnm:
    kl =  os.calcKLDivergence(Po, x, 10)
    KLnm.append(kl)

f = open("./Resultados/sequence_trishift_crissis.txt", 'r')
sc = list(f.read())
sc = [int(x) for x in sc]
f.close()

Psc, alphsc = os.calcProbs(sc, L, q)
Pcond_sc = os.calcCondProbs(Psc, L, alphsc)
Hsc = os.calcCondEntropy(Psc, Pcond_sc, L)
ksc = os.calcKLDivergence(Po,Psc,10)
Ksc = []
for i in range(4,12,2):
	Ksc.append(ksc)

f = open("entropies_trishift.txt", 'w')

l = [str(x) for x in Ho]
l = ','.join(l) + "\n"
f.write(l)

for h in H:
    l = [str(x) for x in h]
    l = ','.join(l) + "\n"
    f.write(l)

for h in Hnm:
    l = [str(x) for x in h]
    l = ','.join(l) + "\n"
    f.write(l)
    
l = [str(x) for x in Hsc]
l = ','.join(l)
f.write(l)

f.close()

f = open("kldivergences_trishift.txt", 'w')
k1 = [str(x) for x in KL]
k1 = ",".join(k1) + "\n"
k2 = [str(x) for x in KLnm]
k2 = ",".join(k2) + "\n"
k3 = [str(x) for x in Ksc]
k3 = ', '.join(k3)
f.write(k1)
f.write(k2)
f.write(k3)
f.close()
    
A = []
a = np.correlate(so, so, 'full')
A.append(a)

for x in s:
	a = np.correlate(x, x, 'full')
	A.append(a)

for x in snm:
	a = np.correlate(x, x, 'full')
	A.append(a)

a = np.correlate(sc, sc, 'full')
A.append(a)

f = open("./Resultados/correlations_tri.txt", 'w')
for a in A:
	l = [str(x) for x in a]
	l = ",".join(l) + "\n"
	f.write(l)
f.close()
