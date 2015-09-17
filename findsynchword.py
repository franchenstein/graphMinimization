import ptriestate as pts
import candidacytrie as ct

def insertWithPriority(l, el):
    curWeight = len(el.name)
    i = 0
    for e in l:
        if curWeight > len(e.name):
            i += 1
    l.insert(i + 1,el)

def findSynchWord(g, t):
    root = g.states[0]
    toTest = []
    names = [x.name for x in g.states]
    for a in g.alphabet:
        sName = root.nextStateFromEdge(a)
        toTest.append(g.states[names.index(sName)])

    for c in toTest:
        inverseC = c.name[::-1]
        nextCandidate = t.states[0].nextCandidate(inverseC, t.states)
        p = g.compareMorphs(c.outedges, nextCandidate.outedges, 0.95, "chi-squared")
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
    
    r = []
    
    for b in t.states:
        if b.candFlag:
            r.append(b)

    return r        
