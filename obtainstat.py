import random

def calcProbs(data, L):
    l = 1
    stats = []
    while l <= L:
        d = dict()
        r = range(0, len(data) - (l - 1))
        for i in r:
            currentValue = ''.join(str(e) for e in data[i:i+l])
            if currentValue in d:
                d[currentValue] += 1
            else:
                d[currentValue] = 1
        for key in d:
            d[key] = d[key]/float(len(data))
        stats.append(d)
        l += 1
    return stats
    
def evenShift(L, p00):
    count = 1
    out = []
    states = [0, 1]
    #Initialize state:
    r = random.random()
    state = states[0] if r < 0.5 else states[1]
    while count <= L:
        r = random.random()
        if state == states[0]:
            a = 0 if r < p00 else 1
            state = states[0] if r < p00 else states[1]
        else:
            a = 1
            state = states[0]
        out.append(a)
        count +=1
    return out     
