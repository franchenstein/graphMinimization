#!/usr/bin/env
import state
import graph
import probabilisticState
import probabilisticGraph as pg
import ptriestate as pts
import candidacytrie as ct
import findsynchword as fsw

g = pg.ProbabilisticGraph([],[])
g.parseGraphFile("binaryshift.txt")

e = pts.pTrieState(g.states[0].name, g.states[0].outedges, True)
t = ct.CandidacyTrie([e], g.alphabet)

r = fsw.findSynchWord(g, t)
