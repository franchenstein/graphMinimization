#!/usr/bin/env
import graph

def removeUnreachableStates(g):
    aux = [x.outedges for x in g.states]
    reachableStates = []
    for x in aux:
        for y in x:
            if y[1] not in reachableStates:
                reachableStates.append(y[1])
                
    newStates = [x for x in g.states if x.name in reachableStates]
    
    aux = [x.outedges for x in newStates]
    newAlphabet = []
    for x in aux:
        for y in x:
            if y[0] not in newAlphabet:
                newAlphabet.append(y[0])
    
    reducedGraph = graph.Graph(newStates, newAlphabet)
    return reducedGraph
    
g = graph.Graph([],[])
g.parseGraphFile('graph.txt')
g = removeUnreachableStates(g)
g.saveGraphFile('reducedgraph.txt')
