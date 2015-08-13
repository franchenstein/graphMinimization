import random

def evenShift(L, p):
    p00 = p[0]
    count = 0
    out = []
    states = [0, 1]
    #Initialize state:
    r = random.random()
    state = states[0] if r < 0.5 else states[1]
    while count < L:
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
    
def binShift(L, p):
    p00, p11 = p
    out = []
    states = [0, 1]
    #Initialize state:
    r = random.random()
    state = states[0] if r < 0.5 else states[1]
    for x in range(0,L):
        r = random.random()
        if state == states[0]:
            a = 0 if r < p00 else 1
            state = states[0] if r < p00 else states[1]
        else:
            a = 1 if r < p11 else 0
            state = states[1] if r < p11 else states[0]
        out.append(a)
    return out        
