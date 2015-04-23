#!/usr/bin/env
import sys, getopt
import state
import graph
import partition
import partitionset

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
    oldSize = len(g.states)
    newSize = -1
    while oldSize != newSize:
        oldSize = newSize
        g = removeUnreachableStates(g) #Removes unreachable states
        newSize = len(g.states)
    gp = moore(g)
    g = graph.Graph(recoverEdgesForPartition(g, gp), g.alphabet)
    g.saveGraphFile(outFile) #Saves graph to file

def removeUnreachableStates(g):
    '''
    Input: A graph described by the class Graph
    Output: A graph where all unreachable states of the input graph are removed.
    Description: The algorithm goes through all the outedges from each state of 
    the graph. Based on the outedges, it creates a list with all destination 
    states. It then proceeds to run through the graph's states and create a list
    of them which only includes states whose names are on the list of reachable 
    states. The alphabet is updated accordingly. With those two elements, a new 
    reduced graph is created and returned. 
    '''
    
    reachableStates = [] #This will receive the reachable states' names.
    aux = [x.outedges for x in g.states] #Creates a list of all states' outedges.
    
    for outedges in aux: #Goes through each state's outedge list
        for outedge in outedges: #Goes through each outedge in the outedge list
            #Checks if the destination state of the current outedge is already
            #in the list:
            if outedge[1] not in reachableStates:
                #If it is not, it is considered as a new reachable state.
                reachableStates.append(outedge[1])
                
    #A new list of states is created only with states whose names are in 
    #reachableStates            
    newStates = [x for x in g.states if x.name in reachableStates]
    
    #List of outedges lists of the new states:
    aux = [x.outedges for x in newStates]
    newAlphabet = [] #Receives the new alphabet
    for outedges in aux: #Goes through each state's outedge list
        for outedge in outedges: #Goes through each outedge in the outedge list
            #Checks if the outedge label is already in the alphabet:
            if outedge[0] not in newAlphabet:
                #If it's not, it is included to the new alphabet.
                newAlphabet.append(outedge[0])
    
    #Creates a new graph, with no unreachable states:
    reducedGraph = graph.Graph(newStates, newAlphabet)
    return reducedGraph

def coarsestPartition(P, Q):    
    l = []
    for p in P:
         for q in Q:
                 r = intersection(p,q)
                 if r.name:
                    if l:
                        names = [element.name for element in l]
                        if r.name not in names:
                            l.append(r)
                    else:
                        l.append(r)             
    return l
    
def intersection(p1, p2):
    name = ""
    outedges = []    
    for a in p1.name:
        for b in p2.name:
            if (a is not ',') and (a == b):
                if not name:
                    name = a
                else:
                    name = name + "," + a                    
    return partition.Partition(state.State(name, outedges))
                
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
    
def moore(g):
    #Initial partition based on outgoing edges:
    P = initialPartition(g)
    P_alphabet = []
    #The loop will end when no new partitions are acquired:
    while True:
        P_old = P #Stores the current partition before the loop  
        for a in g.alphabet:
            pa = [] #Stores the splitted partitions for the current letter
            for p in P.partitions:
                #Creates partitions based on the follower sets:
                splits = splitting(p, a, g.states)
                #Eliminates empty partitions:
                validSplits = [split for split in splits if split.name != ""]
                #Append the current letter's partitions:
                pa.append(validSplits)            
            Pa = []        
            for q1 in pa:
                for q2 in pa:
                    if q1 != q2:
                        cp = coarsestPartition(q1,q2)
                        Pa = noRedundancy(cp, Pa) 
            P_alphabet.append(Pa)        
        P_b = []            
        for pb1 in P_alphabet:
            for pb2 in P_alphabet:
                if pb1 != pb2:
                    pb = coarsestPartition(pb1, pb2)
                    P_b = noRedundancy(pb, P_b)
                                    
        newPartitions = coarsestPartition(P.partitions, P_b)
        newNames = [p.name for p in newPartitions]
        oldNames = [p.name for p in P_old.partitions]
        if newNames == oldNames:
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

