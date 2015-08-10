from state import State


class Graph:
    '''
    This class represents a graph by a list of states (its nodes) and a list of 
    the letters (the alphabet) from which it is constructed. As the states
    contain the information about the edges, a list of them fully describe a
    graph.
    There are methods to read a list of states from a file and to save it in the
    same format.
    '''
    
    def __init__(self, states, alphabet):
        self.states = states        #Graph's list of states
        self.alphabet = alphabet    #List of letters representing the alphabet
   
    '''
    The following methods construct/save a graph based on a text file. The file
    needs to follow a certain format. Each state is represented like this:
    name
    first_edge_label first_destination_state
    second_edge_label second_destination_state
    .
    .
    .
    last_edge_label last_destination state
    
    The blank line after the last edge is essential, as it is the divider between
    states.
    '''
   
    def parseGraphFile(self, filePath):
        '''
        Input: file path containing a graph formatted as described above.
        Output: Updates the current graph with the structure described in the input.
        '''
        
        with open(filePath) as f:
            lines = f.readlines()   #Creates a list where each element is a line
                                    #from the input file.
                
        i = 0 #This variable indicates which part of the file is being processed.
        outedges = [] #Variable that receives the outgoing edges.
        stateList = [] #List of the states read from the file.
        alph = [] #Alphabet deduced from the file.
        name = '' #This variable will be used to read each state's name.
        
        for line in lines: #Loops for each line in the file
            
            if line == "\n": #Blank line indicates end of a state's description
            
                i = 0 #i is set to 0 so the next loop will start reading the name
                
                #Create a State with the name and outedges read till this point
                stateList.append(State(name, outedges))
                #Resets variables for next loop:
                name = ''
                outedges = []
                
            else:
            
                if i == 0: #This indicates that we're searching for the name                                 
                    i = i + 1 #The next loop will start searching outedges
                    j = 0       
                    
                    #Appends the name's characters until the end of the line:
                    while line[j] != '\n':
                        name = name + line[j]
                        j = j + 1
                
                else: #i != 0 means we're searching for outedges  
                    outEdge = line.split()
                    if outEdge[0] not in alph:
                        alph.append(outEdge[0])   
                    outedges.append(tuple(outEdge))
        
        #After going through the file, updates the graph:        
        self.states = stateList        
        self.alphabet = alph
        
    def saveGraphFile(self, filePath):
        '''
        Input: File path where the graph will be saved.
        Output: File containing the description of the graph as stated above.
        '''
        
        f = open(filePath, 'w') #File open as writeble.
        lines = [] #Each element will be a line to be written in the file.
        
        #Loops through all states:
        for s in self.states:
            lines.append(s.name + '\n') #The first element will be the name
            #Each out edge will be appended as the edge space destination:
            for e in s.outedges:
                i = 1
                edgeline = ''
                for element in e:
                    conn = ' ' if i < len(e) else '\n'
                    edgeline = edgeline + element + conn
                    i += 1
                lines.append(edgeline)
            lines.append('\n') #Blank line indicating end of state
            
        f.writelines(lines) #Lines are written to file
        f.close
        
    def removeUnreachableStates(self):
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
        
        oldSize = len(self.states)
        reachableStates = [] #This will receive the reachable states' names.
        aux = [x.outedges for x in self.states] #Creates a list of all states' outedges.
        
        for outedges in aux: #Goes through each state's outedge list
            for outedge in outedges: #Goes through each outedge in the outedge list
                #Checks if the destination state of the current outedge is already
                #in the list:
                if outedge[1] not in reachableStates:
                    #If it is not, it is considered as a new reachable state.
                    reachableStates.append(outedge[1])
                    
        #A new list of states is created only with states whose names are in 
        #reachableStates            
        newStates = [x for x in self.states if x.name in reachableStates]
        
        #List of outedges lists of the new states:
        aux = [x.outedges for x in newStates]
        newAlphabet = [] #Receives the new alphabet
        for outedges in aux: #Goes through each state's outedge list
            for outedge in outedges: #Goes through each outedge in the outedge list
                #Checks if the outedge label is already in the alphabet:
                if outedge[0] not in newAlphabet:
                    #If it's not, it is included to the new alphabet.
                    newAlphabet.append(outedge[0])
        
        #Creates a new graph, without previous unreachable states:
        reducedGraph = Graph(newStates, newAlphabet)
        newSize = len(reducedGraph.states)
        
        if (oldSize != newSize):
            reducedGraph = reducedGraph.removeUnreachableStates()
        
        return reducedGraph
