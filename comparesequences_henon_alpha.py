#!/usr/bin/env
import obtainstat as os
import matplotlib as plt
import multiprocessing as mp

def autocorrelate(x, upTo):
    A = []
    for i in range(0,upTo):
        acc = 0
        for j in range(0, len(x) - i):
            acc += x[i + j]*x[j]
        A.append(acc)
    return A

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
Ao = autocorrelate(so, 200)

f1 = "./Resultados/sequence_henon_generated_alpha"
f2 = "_10000000.txt"
f2nm = "_10000000_NoMoore.txt"
alpharange = [0.9, 0.95, 0.99]

s = []
for i in alpharange:
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
A = []
for x in s:
    p, alph = os.calcProbs(x, L, q)
    P.append(p) 
    pcond = os.calcCondProbs(p, L, alph)
    Pcond.append(pcond)
    h = os.calcCondEntropy(p, pcond, L)
    H.append(h)
    a = autocorrelate(x, 200)
    A.append(a)
    
KL = []
for x in P:
    kl =  os.calcKLDivergence(Po, x, 10)
    KL.append(kl)

snm = []
for i in alpharange:
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
Anm = []
for x in snm:
    p, alph = os.calcProbs(x, L, q)
    Pnm.append(p) 
    pcond = os.calcCondProbs(p, L, alph)
    Pcond_nm.append(pcond)
    h = os.calcCondEntropy(p, pcond, L)
    Hnm.append(h)
    anm = autocorrelate(x, 200)
    Anm.append(anm)
    
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
Asc = autocorrelate(sc, 200)
	
f = open("./Resultados/sequence_henon_dmarkov_D9_10000000.txt", 'r')
sd9 = list(f.read())
sd9 = [int(x) for x in sd9]
f.close()

Pd9, alphd9 = os.calcProbs(sd9, L, q)
Pcond_d9 = os.calcCondProbs(Pd9, L, alphd9)
Hd9 = os.calcCondEntropy(Pd9, Pcond_d9, L)
kd9 = os.calcKLDivergence(Po,Pd9,10)
Kd9 = []
for i in range(6,14,2):
	Kd9.append(kd9)
Ad9 = autocorrelate(sd9, 200)
	
f = open("./Resultados/sequence_henon_dmarkov_D10_10000000.txt", 'r')
sd10 = list(f.read())
sd10 = [int(x) for x in sd10]
f.close()

Pd10, alphd10 = os.calcProbs(sd10, L, q)
Pcond_d10 = os.calcCondProbs(Pd10, L, alphd10)
Hd10 = os.calcCondEntropy(Pd10, Pcond_d10, L)
kd10 = os.calcKLDivergence(Po,Pd10,10)
Kd10 = []
for i in range(6,14,2):
	Kd10.append(kd10)
Ad10 = autocorrelate(sd10, 200)

f = open("./Resultados/entropies_henon.txt", 'w')

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
    
l = [str(x) for x in Hd9]
l = ','.join(l) + "\n"
f.write(l)
    
l = [str(x) for x in Hd10]
l = ','.join(l) + "\n"
f.write(l)

f.close()

f = open("kldivergences_henon.txt", 'w')
k1 = [str(x) for x in KL]
k1 = ",".join(k1) + "\n"
k2 = [str(x) for x in KLnm]
k2 = ",".join(k2) + "\n"
k3 = [str(x) for x in Ksc]
k3 = ', '.join(k3) + "\n"
k4 = [str(x) for x in Kd9]
k4 = ', '.join(k4) + "\n"
k5 = [str(x) for x in Kd10]
k5 = ', '.join(k5)
f.write(k1)
f.write(k2)
f.write(k3)
f.write(k4)
f.write(k5)
f.close()

f = open("autocorrelations_henon.txt", 'w')
a0 = [str(x) for x in Ao]
a0 = ",".join(a0) + "\n"
f.write(a0)
for a in A:
    l = [str(x) for x in a]
    l = ",".join(l) + "\n"
    f.write(l)
for a in Anm:
    l = [str(x) for x in a]
    l = ",".join(l) + "\n"
    f.write(l)
asc = [str(x) for x in Asc]
l = ",".join(asc) + "\n"
f.write(l)
ad9 = [str(x) for x in Ad9]
l = ",".join(ad9) + "\n"
f.write(l)
ad10 = [str(x) for x in Ad10]
l = ",".join(ad10) + "\n"
f.write(l)
    
