#!/usr/bin/env
import obtainstat as os
import matplotlib as plt
import multiprocessing as mp

q = mp.Queue()

so = os.generate("even", 10000000, [0.99])

Po, alpho = os.calcProbs(so, 12, q)
Pcondo = os.calcCondProbs(Po, 12, alpho)
Ho = os.calcCondEntropy(Po, Pcondo, 12)

f1 = "./Resultados/sequence_evenshift_generated_L"
f2 = "_10000000.txt"
f2nm = "_10000000_NoMoore.txt"

s = []
for i in range(4,14,2):
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
    p, alph = os.calcProbs(x, 12, q)
    P.append(p) 
    pcond = os.calcCondProbs(p, 12, alph)
    Pcond.append(pcond)
    h = os.calcCondEntropy(p, pcond, 12)
    H.append(h)
    
KL = []
for x in P:
    kl =  os.calcKLDivergence(Po, x, 10)
    KL.append(kl)

snm = []
for i in range(4,14,2):
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
    p, alph = os.calcProbs(x, 12, q)
    Pnm.append(p) 
    pcond = os.calcCondProbs(p, 12, alph)
    Pcond_nm.append(pcond)
    h = os.calcCondEntropy(p, pcond, 12)
    Hnm.append(h)
    
KLnm = []
for x in Pnm:
    kl =  os.calcKLDivergence(Po, x, 10)
    KLnm.append(kl)
    

f = open("entropies.txt", 'w')

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
    
f.close()

f = open("kldivergences.txt", 'w')
k1 = [str(x) for x in KL]
k1 = ",".join(k1) + "\n"
k2 = [str(x) for x in KLnm]
k2 = ",".join(k2) + "\n"
f.write(k1)
f.write(k2)
f.close()

    
