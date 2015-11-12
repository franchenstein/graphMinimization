from candidacytrie import *
from probabilisticGraph import *


def reverse(descendants, tree):
    reversed = []
    for d in descendants:
        r = [s for s in tree.states if s.name == d.name[::-1]]
        for x in r:
            reversed.append(x)
    return reversed


def findSynchWords(L, synchTrie, testTree):
    # Initialization:
    ST = [synchTrie.root()]
    TT = [testTree.root()]
    expand = testTree.expand(testTree.root())
    for e in expand:
        TT.append(e)
    testedPairs = []
    # Main Loop:
    while True:
        if ST:
            currentCandidate = ST.pop(0)
        else:
            break
        suffixFound = []
        l = currentCandidate.nameLength()
        if l < L:
            toCompare = [s for s in TT if ((s.nameLength() > l) and
                                           (s not in suffixFound) and
                                           ((s.name, currentCandidate.name) not in testedPairs))]
            toCompareCounter = 0
            for h in toCompare:
                if h.isSuffix(currentCandidate):
                    suffixFound.append(h)
                    p = testTree.compareMorphs(currentCandidate.outedges, h.outedges, 0.99, "chi-squared")
                    testedPairs.append((h, currentCandidate))
                    if not p[0]:
                        descendants = synchTrie.expand(currentCandidate, L)
                        revDescendants = reverse(descendants, testTree)
                        for r in revDescendants:
                            exps = testTree.expand(r)
                            for e in exps:
                                if e not in TT:
                                    TT.append(e)
                        synchTrie.markUntested()
                        break
                toCompareCounter += 1
                if toCompareCounter == len(toCompare):
                    synchTrie.markTested(currentCandidate)
        ST = synchTrie.validStates()
    synchWords = [s for s in synchTrie.states if s.candidacy == True]
    return synchWords
