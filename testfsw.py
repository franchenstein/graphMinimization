#!/usr/bin/env
import state
import graph
import probabilisticState
import probabilisticGraph as pg
import ptriestate as pts
import candidacytrie as ct
import findsynchwords as fsw

testTree = pg.ProbabilisticGraph([],[])
testTree.parseGraphFile("binshift_1000000_8.txt")
synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
L = 4

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for binary shift, 10000000 sequence, L = 8, L1 = 4. \n"
for x in r:
	print x.name

print "\n"

L = 5

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for binary shift, 10000000 sequence, L = 8, L1 = 5. \n"
for x in r:
	print x.name

print "\n"

synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
L = 6

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for binary shift, 10000000 sequence, L = 8, L1 = 6. \n"
for x in r:
	print x.name

print "\n"

testTree.parseGraphFile("evenshift_1000000_8.txt")
synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
L = 4

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for even shift, 10000000 sequence, L = 8, L1 = 4. \n"
for x in r:
	print x.name

print "\n"

L = 5

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for even shift, 10000000 sequence, L = 8, L1 = 5. \n"
for x in r:
	print x.name

print "\n"

synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
L = 6

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for even shift, 10000000 sequence, L = 8, L1 = 6. \n"
for x in r:
	print x.name

print "\n"

testTree.parseGraphFile("trishift_1000000_8.txt")
synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
L = 4

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for tri shift, 10000000 sequence, L = 8, L1 = 4. \n"
for x in r:
	print x.name

print "\n"

L = 5

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for tri shift, 10000000 sequence, L = 8, L1 = 5. \n"
for x in r:
	print x.name

print "\n"

L = 6

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for tri shift, 10000000 sequence, L = 8, L1 = 6. \n"
for x in r:
	print x.name

print "\n"

testTree.parseGraphFile("ternaryshift_10000000_10.txt")
synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
L = 4

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for ternary shift, 10000000 sequence, L = 8, L1 = 4. \n"
for x in r:
	print x.name

print "\n"

L = 5

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for ternary shift, 10000000 sequence, L = 8, L1 = 5. \n"
for x in r:
	print x.name

print "\n"

L = 6

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Results for ternary shift, 10000000 sequence, L = 8, L1 = 6. \n"
for x in r:
	print x.name

print "\n"