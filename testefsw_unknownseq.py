#!/usr/bin/env
import state
import graph
import probabilisticState
import probabilisticGraph as pg
import ptriestate as pts
import candidacytrie as ct
import findsynchwords as fsw

testTree = pg.ProbabilisticGraph([],[])


testTree.parseGraphFile("teste10dB_L12.txt")
synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)

L = 8  

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Teste 10 dB L = 15, L1 = 8"
for x in r:
	print x.name

print "\n"

synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)

L = 9  

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Teste 10 dB L = 15, L1 = 9"
for x in r:
	print x.name

print "\n"

synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)

L = 10

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Teste 10 dB L = 15, L1 = 10"
for x in r:
	print x.name

print "\n"

testTree.parseGraphFile("teste15dB_L15.txt")
synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)

L = 8

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Teste 15 dB L = 15, L1 = 8"
for x in r:
	print x.name

print "\n"

synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)

L = 9

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Teste 15 dB L = 15, L1 = 9"
for x in r:
	print x.name

print "\n"

synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)

L = 10

r = fsw.findSynchWords(L, synchTrie, testTree)

print "Teste 15 dB L = 15, L1 = 10"
for x in r:
	print x.name

print "\n"
