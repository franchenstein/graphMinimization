#!/usr/bin/env
import obtainstat as os
import matplotlib as plt
import multiprocessing as mp

q = mp.Queue()

f = open("../Sequencias/MH6.dat", 'r')
so = ""
for l in f.readlines():
	so += l[:len(l)-1]
f.close()

so = list(so)
for i in range(0,len(so)):
    so[i] = int(so[i])

L = 15
Po, alpho = os.calcProbs(so, L, q)
Pcondo = os.calcCondProbs(Po, L, alpho)
Ho = os.calcCondEntropy(Po, Pcondo, L)

f1 = "./Resultados/sequence_henon_generated_L"
f2 = "_10000000.txt"
f2nm = "_10000000_NoMoore.txt"

s = []
for i in range(6,14,2):
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
for i in range(6,14,2):
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

f = open("./Resultados/sequence_henon_crissis.txt", 'r')
sc = list(f.read())
sc = [int(x) for x in sc]
f.close()

Psc, alphsc = os.calcProbs(sc, L, q)
Pcond_sc = os.calcCondProbs(Psc, L, alphsc)
Hsc = os.calcCondEntropy(Psc, Pcond_sc, L)
ksc = os.calcKLDivergence(Po,Psc,10)
Ksc = []
for i in range(6,14,2):
	Ksc.append(ksc)

f = open("entropies_henon.txt", 'w')

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

f = open("kldivergences_henon.txt", 'w')
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
    
