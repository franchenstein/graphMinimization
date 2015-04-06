from state import State


class Graph:
    '''
    Graph
    Description:
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
    #Input: file path containing a graph formatted as described above.
    #Output: Updates the current graph with the structure described in the input.
    
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
                    j = 0
                    
                    #Initializes and edge with blank attributes:
                    edge = ''
                    stateName = ''
                   
                    #Everything before the space is the edge's label
                    while line[j] != ' ':
                        edge = edge + line[j]
                        j = j + 1
                    
                    #This will include the label in the new alphabet:
                    if edge not in alph:
                        alph.append(edge)
                    
                    k = j + 1 #The loop will continue after the space.
                        
                    #The destination state's name is between the space and the
                    #end of the line.    
                    while line[k] != '\n':
                        stateName = stateName + line[k]
                        k = k + 1
                        
                    #Adds the newly created outedge to the list.    
                    outedges.append((edge, stateName))
        
        #After going through the file, updates the graph:        
        self.states = stateList        
        self.alphabet = alph
        
    def saveGraphFile(self, filePath):
    #Input: File path where the graph will be saved.
    #Output: File containing the description of the graph as stated above.
        
        f = open(filePath, 'w') #File open as writeble.
        lines = [] #Each element will be a line to be written in the file.
        
        #Loops through all states:
        for s in self.states:
            lines.append(s.name + '\n') #The first element will be the name
            #Each out edge will be appended as the edge space destination:
            for e in s.outedges:
                lines.append(e[0] + ' ' + e[1] + '\n')
            lines.append('\n') #Blank line indicating end of state
            
        f.writelines(lines) #Lines are written to file
        f.close
