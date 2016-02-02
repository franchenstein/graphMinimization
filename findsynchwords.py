from candidacytrie import *
from probabilisticGraph import *


def reverse(descendants, tree):
    reversed = []
    for d in descendants:
        r = [s for s in tree.states if s.name == d.name[::-1]]
        for x in r:
            reversed.append(x)
    return reversed

def expandtrees(s, trie, tree, testlist, L):
    descendants = trie.expand(s, L)
    revdescendants = reverse(descendants, tree)
    for r in revdescendants:
        n = trie.shortestValidSuffix(r.name)
        if n == r.name:
            exps = tree.expand(r)
            for e in exps:
                if e not in testlist:
                    testlist.append(e)


def findSynchWords(L, synchTrie, testTree, alpha, testType):
    # Initialization:
    ST = [synchTrie.root()]
    ST[0].candidacy = True
    TT = [testTree.root()]
    expand = testTree.expand(testTree.root())
    for e in expand:
        TT.append(e)
    testedPairs = []
    suffixFound = []
    # Main Loop:
    while True:
        if ST:
            currentCandidate = ST.pop(0)
        else:
            break
        l = currentCandidate.nameLength()
        if l < L:
            toCompare = [s for s in TT if ((s.nameLength() > l) and
                                           (s.name not in suffixFound) and
                                           ((s.name, currentCandidate.name) not in testedPairs))]
            toCompareCounter = 0
            for h in toCompare:
                if synchTrie.isSuffix(h.name, currentCandidate.name):
                    p = testTree.compareMorphs(currentCandidate.outedges, h.outedges, alpha, testType)
                    (a, b) = (h.name, currentCandidate.name)
                    if (a,b) not in testedPairs:
                        testedPairs.append((a, b))
                    if not p[0]:
                        expandtrees(currentCandidate, synchTrie, testTree, TT, L)
                        synchTrie.markUntested()
                        break
                    else:
                        suffixFound.append(h.name)
                toCompareCounter += 1
                if toCompareCounter == len(toCompare):
                    testedNames = list(set([x[1] for x in testedPairs]))
                    if currentCandidate.name in testedNames:
                        synchTrie.markTested(currentCandidate)
                    else: 
                        currentCandidate.candidacy = False
        ST = synchTrie.validStates()
    synchWords = [s for s in synchTrie.states if s.candidacy and s.tested]
    return synchWords  
