#!/usr/bin/env
import numpy as np

f = open("../Sequencias/MH6.dat", 'r')
so = ""
for l in f.readlines():
	so += l[:len(l)-1]
f.close()

so = list(so)
for i in range(0,len(so)):
	so[i] = int(so[i])

f1 = "./Resultados/sequence_henon_generated_L"
f2 = "_10000000.txt"
f2nm = "_10000000_NoMoore.txt"

s = []
for i in range(4, 12, 2):
	f = f1+str(i)+f2
	fi = open(f)
	s.append(list(fi.read()))
	fi.close()

for x in s:
	for i in range(0,len(x)):
		x[i] = int(x[i])

snm = []
for i in range(4,12,2):
	f = f1+str(i)+f2nm
	fi = open(f)
	snm.append(list(fi.read()))
	fi.close()

for x in snm:
	for i in range(0, len(x)):
		x[i] = int(x[i])

f = open("./Resultados/sequence_henon_crissis.txt", 'r')
sc = list(f.read())
sc = [int(x) for x in sc]
f.close()

f = open("./Resultados/correlations_henon.txt", 'w')
A = []

a = np.correlate(so, so, "full")
A.append(a)

for x in s:
	a = np.correlate(x,x,"full")
	A.append(a)

for x in snm:
	a = np.correlate(x, x, "full")
	A.append(a)

a = np.correlate(sc, sc, "full")
A.append(a)

for a in A:
	l = [str(x) for x in a]
	l = ','.join(l) + '\n'
	f.write(l)

f.close()

