#!/usr/bin/env
import graph

""" 
This script will take a graph described in an user-defined filepath and create
a structure corresponding to that graph. It will then apply a function to remove
unreachable states and then a minimization via Moore's or Hopcroft's algorithm,
as desired by the user.
"""

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
    
#Main script:    
g = graph.Graph([],[]) #Blank graph
g.parseGraphFile('graph.txt') #Updated with graph on file
g = removeUnreachableStates(g) #Removes unreachable states
g.saveGraphFile('reducedgraph.txt') #Saves graph to file
