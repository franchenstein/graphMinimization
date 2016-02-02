import ptriestate as pts
import candidacytrie as ct

def insertWithPriority(l, el):
    curWeight = len(el.name)
    i = 0
    for e in l:
        if curWeight > len(e.name):
            i += 1
    l.insert(i + 1,el)

def findSynchWord(w, g, t, alpha, testType):
    root = g.states[0]
    toTest = []
    names = [x.name for x in g.states]
    for a in g.alphabet:
        sName = root.nextStateFromEdge(a)
        toTest.append(g.states[names.index(sName)])

    tested = {}
    while toTest:
        c = toTest.pop(0)
        inverseC = c.name[::-1]
        nextCandidate = t.states[0].nextCandidate(inverseC, t.states)
        p = g.compareMorphs(c.outedges, nextCandidate.outedges, alpha, testType)    
        if p[0]:
            insertWithPriority(toTest, c)
        else:            
            nexts = t.expandState(nextCandidate, g)
            newToTest = []
            for n in nexts:
                s = g.states[names.index(n)]
                for a in g.alphabet:
                    nc = s.nextStateFromEdge(a)
                    newToTest.append(g.states[names.index(nc)])
                    
            toTest = [x for x in toTest if x.name not in nexts]
                    
            for e in newToTest:
                insertWithPriority(toTest, e)

            k = tested.keys()
            kn = [x for x in k if x > 1 and x < len(c.name)]

            for y in kn:
                for z in tested[y]:
                    insertWithPriority(toTest, z)

        if len(c.name) in tested.keys():
            tested[len(c.name)].append(c)
        else:
            tested[len(c.name)] = [c]
    
    r = []
    
    for b in t.states:
        if b.candFlag:
            r.append(b)

    return r        
