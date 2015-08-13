#!/usr/bin/env
import sys, getopt
import probabilisticState
import probabilisticGraph
import partition
import partitionset
import probabilisticPartition

""" 
This script will take a graph described in an user-defined filepath and create
a structure corresponding to that graph. It will then apply a function to remove
unreachable states and then a minimization via Moore's or Hopcroft's algorithm,
as desired by the user.
"""

def main(argv):
    inFile, outFile = readInput(argv)
    g = probabilisticGraph.ProbabilisticGraph([],[]) #Blank graph
    g.parseGraphFile(inFile) #Updated with graph on file
    g = g.removeUnreachableStates()
    gp = moore(g)
    g = probabilisticGraph.ProbabilisticGraph(recoverEdgesForPartition(g, gp), g.alphabet)
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
    name = ""
    p1names = p1.name.split(",")
    p2names = p2.name.split(",")
    for a in p1names:
        for b in p2names:
            if a == b:
                if not name:
                    name = a
                else:
                    name = name + "," + a                  
    return partition.Partition(probabilisticState.ProbabilisticState(name, []))
                
def splitting(p, a, Q):
    p1 = partition.Partition(probabilisticState.ProbabilisticState("",[]))
    p2 = partition.Partition(probabilisticState.ProbabilisticState("",[]))    
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

    states = g.states
    partitions = [probabilisticPartition.ProbabilisticPartition(states.pop(0))]
    for s in states:
        i = 0
        for p in partitions:
            res = g.compareMorphs(s.outedges, p.morph(), 0.95, 'chi-squared')
            if res[0]:
                p.addToPartition(s)
                break
            i += 1
        if i == len(partitions):
            partitions.append(probabilisticPartition.ProbabilisticPartition(s))
            
    for p in partitions:
        print "----------------------------------------------"
        print "|name: " + p.name
        print "|edges: "
        for e in p.outedges:
            print "|     " + str(e)
        print "----------------------------------------------"
        print "\n"
    
    return partitionset.PartitionSet(partitions)                   
    
def moore(g):
    #Initial partition based on outgoing edges:
    P = initialPartition(g)   
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
                validSplits = [split for split in splits if split.name != ""]
                #Append the current letter's partitions:
                pa.append(validSplits)
                        
            Pa = pa[0]
            for q in pa[1:]:
                cp = coarsestPartition(Pa, q)
                Pa = noRedundancy(cp, Pa)
            P_alphabet.append(Pa)         
        
        P_b = P_alphabet[0]
        for pb in P_alphabet[1:]:
            cp = coarsestPartition(P_b, pb)
            P_b = noRedundancy(cp, P_b)    
                                   
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
        newStates.append(probabilisticState.ProbabilisticState(p.name, newEdges))
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

