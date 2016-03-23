#!/usr/bin/env
import sys, getopt
import state
import graph
import partition
import partitionset
import probabilisticGraph as pg
import probabilisticState as ps

""" 
This script will take a graph described in an user-defined filepath and create
a structure corresponding to that graph. It will then apply a function to remove
unreachable states and then a minimization via Moore's or Hopcroft's algorithm,
as desired by the user.
"""

def main(argv):
    inFile, outFile = readInput(argv)
    g = graph.Graph([],[]) #Blank graph
    g.parseGraphFile(inFile) #Updated with graph on file
    g = g.removeUnreachableStates()
    P = initialPartition(g)
    gp = moore(P, g)
    g = graph.Graph(recoverEdgesForPartition(g, gp), g.alphabet)
    g.saveGraphFile(outFile) #Saves graph to file

def coarsestPartition(P, Q):    
    l = []
    for p in P:
         for q in Q:
                 r = intersection(p,q)
                 if r.name: #Empty intersections are disregarded.
                    if l:
                        names = [element.name for element in l]
                        if r.name not in names:
                            l.append(r)
                    else:
                        l.append(r)             
    return l
    
def intersection(p1, p2):
    name = []
    for a in p1.name:
        for b in p2.name:
            if a == b:
                if not name:
                    name = [a]
                else:
                    name.append(a) 
    if name:
        p = partition.Partition(state.State(name.pop(0), []))
        for n in name:
            p.addToPartition(state.State(n,[])) 
    else:
        p = partition.Partition(state.State(name,[]))             
    return p
                
def splitting(p, a, Q):
    p1 = partition.Partition(state.State("",[]))
    p2 = partition.Partition(state.State("",[]))    
    for q in Q:
        possibleLabels = [edge[0] for edge in q.outedges]
        if a in possibleLabels:
            if q.nextStateFromEdge(a) in p.name:
                p1.addToPartition(q)
            else:
                p2.addToPartition(q)
        else:
            p1.addToPartition(q)
            p2.addToPartition(q)                
    return [p1, p2] 
    
def initialPartition(g):
    partitions = []
    for state in g.states:
        sEdgeLetters = []
        for edge in state.outedges:
            if edge[0] not in sEdgeLetters:
                sEdgeLetters.append(edge[0])
        if not partitions:
            partitions.append(partition.Partition(state))
        else:
            i = 0
            for p in partitions:
                pEdgeLetters = []
                for edge in p.outedges:
                    if edge[0] not in pEdgeLetters:
                        pEdgeLetters.append(edge[0])
                if sEdgeLetters == pEdgeLetters:
                    p.addToPartition(state)
                    break
                else:
                    i += 1
            if i == len(partitions):
                partitions.append(partition.Partition(state))              
    
    P = partitionset.PartitionSet(partitions)
    return P            
    
def moore(P, g):
    #Initial partition based on outgoing edges:
    #P = initialPartition(g)   
    #The loop will end when no new partitions are acquired:
    while True:
        P_old = P #Stores the current partition before the loop
        P_alphabet = []  
        for a in g.alphabet:
            pa = [] #Stores the splitted partitions for the current letter
            for p in P.partitions:
                #Creates partitions based on the follower sets:
                splits = splitting(p, a, g.states)
                #Eliminates empty partitions:
                validSplits = [split for split in splits if split.name]
                #Append the current letter's partitions:
                pa.append(validSplits)
            
            Pa = pa[0]
            for q in pa[1:]:
                cp = coarsestPartition(Pa, q)
                #Pa = noRedundancy(cp, Pa)
                Pa = cp
            P_alphabet.append(Pa)         

        P_b = P_alphabet[0]
        for pb in P_alphabet[1:]:
            cp = coarsestPartition(P_b, pb)
            #P_b = noRedundancy(cp, P_b)
            P_b = cp
        
        newPartitions = coarsestPartition(P.partitions, P_b)
        newNames = [tuple(p.name) for p in newPartitions]
        oldNames = [tuple(p.name) for p in P_old.partitions]
        if set(newNames) == set(oldNames):
            break
        else:
            P.partitions = newPartitions           
    return P 
    
def noRedundancy(l1, l2):
    for element in l1:
        if not l2:
            l2.append(element)
        else:
            names = [el.name for el in l2]
            if element.name not in names:
                l2.append(element)
    return l2
    
def recoverEdgesForPartition(g, ps):
    partitionNames = [p.name for p in ps.partitions]
    newStates = []
    for p in ps.partitions:
        newEdges = []
        for s in g.states:
            if s.name in p.name:
                for edge in s.outedges:
                    for name in partitionNames:
                        if edge[1] in name:
                            newEdges.append((edge[0], name))
                            break 
                break       
        newStates.append(state.State(p.name, newEdges))
    return newStates
    
def isSuffix(w,n):
    if len(w) > len(n):
        return False
    else:
        nSuffix = n[-len(w):]
        return w == nSuffix
        
def minimizeFromSynchWords(g, synchlist):
    s = [x for x in g.states if x.name in synchlist]
    states = []
    while True:
       if not s:
            break
       else:
            aux = s.pop()
            nexts = [x[1] for x in aux.outedges]
            i = 0
            oedges = []
            for n in nexts:
                e = n
                for w in synchlist:
                    if isSuffix(w,n):
                        e = w
                        break
                edge = (aux.outedges[i][0], e, aux.outedges[i][2])
                oedges.append(edge)
                i += 1
            newState = ps.ProbabilisticState(aux.name, oedges)
            states.append(newState)
            statesNames = [x.name for x in states]
            newNexts = [x[1] for x in newState.outedges if x[1] not in statesNames]
            for n in newNexts:
                v = g.stateNamed(n)
                if v:
                    s.append(g.stateNamed(n))
    h = pg.ProbabilisticGraph(states, g.alphabet)
    return h               
                            
def readInput(argv):
    inFile = ""
    outFile = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print 'graphMinimization.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'graphMinimization.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inFile = arg
        elif opt in ("-o", "--ofile"):
            outFile = arg
    return [inFile, outFile]
        
if __name__ == "__main__":
    main(sys.argv[1:])   

