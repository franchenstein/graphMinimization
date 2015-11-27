import random
from enum import Enum

class States(Enum):
    A = 1
    B = 2
    C = 3
    D = 4

def ternDistribution(p0, p1):
    r = random.random()
    if r < p0:
        return 0
    elif r < p0 + p1:
        return 1
    else:
        return 2

def evenShift(L, p):
    p00 = p[0]
    count = 0
    out = []
    #Initialize state:
    r = random.randint(1,2)
    state = States(r)
    for i in range(0, L):
        r = random.random()
        if state == States.A:
            a = 0 if r < p00 else 1
            state = States.A if r < p00 else States.B
        else:
            a = 1
            state = States.A
        out.append(a)
    return out
    
def binShift(L, p):
    p00, p11 = p
    out = []
    #Initialize state:
    r = random.randint(1,2)
    state = States(r)
    for x in range(0, L):
        r = random.random()
        if state == States.A:
            a = 0 if r < p00 else 1
            state = States.A if r < p00 else States.B
        else:
            a = 1 if r < p11 else 0
            state = States.A if r < p11 else States.B
        out.append(a)
    return out     
    
def triShift(L, p):
    p0, p1, p2 = p
    out = []
    #Initialize state:
    r = random.randint(1,3)
    state = States(r)
        
    for x in range(0,L):
        r = random.random()
        if state == States.A:
            a = 0 if r < p0 else 1
            state = States.A if r < p0 else States.B
        elif state == States.B:
            a = 0 if r < p1 else 1
            state = States.C if r < p1 else States.A
        else:
            a = 0 if r < p2 else 1
            state = States.A if r < p2 else States.C
        out.append(a)
    return out 

def ternaryShift(L, p):
    p0A, p1A, p0B, p1B, p0C, p1C, p0D, p1D = p
    r = random.randint(1,4)
    state = States(r)
    out = []

    for x in range(0, L):
        r = random.random()
        if state == States.A:
            r = ternDistribution(p0A, p1A)
            if r == 0:
                a = 0
                state = States.D
            elif r == 1:
                a = 1
                state = States.C
            else:
                a = 2
                state = States.A
        elif state == States.B:
            r = ternDistribution(p0B, p1B)
            if r == 0:
                a = 0
                state = States.B
            elif r == 1:
                a = 1
                state = States.A
            else:
                a = 2
                state = States.C
        elif state == States.C:
            r = ternDistribution(p0C, p1C)
            if r == 0:
                a = 0
                state = States.B
            elif r == 1:
                a = 1
                state = States.C
            else:
                a = 2
                state = States.D
        elif state == States.D:
            r = ternDistribution(p0D, p1D)
            if r == 0:
                a = 0
                state = States.A
            elif r == 1:
                a = 1
                state = States.B
            else:
                a = 2
                state = States.A
        out.append(a)
    return(out)