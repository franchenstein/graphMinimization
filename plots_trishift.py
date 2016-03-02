#!/usr/bin/env
import matplotlib.pyplot as plt

with open('entropies_trishift.txt', 'r') as f:
    h = f.readlines()
f.close()

with open('kldivergences_trishift.txt', 'r') as f:
    k = f.readlines()
f.close()

H = []
for x in h:
    y = x[:-1].split(',')
    y = [float(z) for z in y]
    H.append(y)
    
K = []
for x in k:
    y = x[:-1].split(',')
    y = [float(z) for z in y]
    K.append(y)
    
x = range(1,16)    

plt.plot(x,H[0], 'k', label = "Original Sequence")
plt.plot(x,H[1], 'b', label = "L=6, 44 states")
plt.plot(x,H[5], 'b--', label = "L=6, No Moore, 13 states")
plt.plot(x,H[2], 'r', label = "L=8, 111 states")
plt.plot(x,H[6], 'r--', label = "L=8, No Moore, 17 states")
plt.plot(x,H[3], 'g', label = "L=10, 414 states")
plt.plot(x,H[7], 'g--', label = "L=10, No Moore, 18 states")
plt.plot(x,H[4], 'y', label = "L=12, 1466 states")
plt.plot(x,H[8], 'y--', label = "L=12, No Moore, 18 states")
plt.plot(x,H[9], 'm', label = "Crissis, 6 states")
legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
plt.show()

x = range(6,14,2)
plt.plot(x,K[0], label = "Original Sequence vs. PFSA w/ Moore")
plt.plot(x,K[1], label = "Original Sequence vs. PFSA No Moore")
plt.plot(x,K[2], label = "Original Sequence vs. PFSA Crissis")
legend = plt.legend(loc='upper right', shadow=False, fontsize='medium')
plt.show()
