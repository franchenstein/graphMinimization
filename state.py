class State:
    '''
    This class represents a state or node in a graph. This representation is
    done using a name (or a label) to refer to the state and a list of its 
    outgoing edges. The outgoing edges list is a list of tuples where the first
    element is the letter from the automata/shift space alphabet labeling the
    edge and the second element is the name of the state to where that edge
    leads.
    There are methods to retrieve the destination of an outgoing edge based on
    the letter of the alphabet labeling that edge and, respectively, to retrieve
    a state name from the letter labeling an edge.
    '''
    
    def __init__(self, name, outedges):
        self.name = name            #The state's name/label
        self.outedges = outedges    #List of outgoing edges
            
    def nextStateFromEdge(self, letter):
        '''
        Input: letter from the graph's alphabet
        Output: Destination from the edge containing the input letter as label.
        '''
    
        #Finds and returns a state name from outedges based on a letter.
        matches = [x[1] for x in self.outedges if x[0] == letter]
        return matches[0]
        
    def edgeThatLeadsToState(self, stateName):
        '''
        Input: Destination state's name.
        Output: Label from the edge that goes to the desired state.
        '''
    
        #Finds and returns an edge label from outedges based on a state name.
        matches = [x[0] for x in self.outedges if x[1] == stateName]
        return matches[0]
        
    def obtainChildren(self, g):
        '''
        Input: graph in which the children states from the current states will
               be searched.
        Output: list with current state's children
        '''
        childrenNames = [o[1] for o in self.outedges]
        children = [s for s in g.states if s.name in childrenNames]
        return children   

    def nameLength(self):
        if self.name == 'e':
            return 0
        else:
            return len(self.name)

    def isSuffix(self, s):
        if s == 'e':
            return True
        else:
            return self.name.endswith(s[::-1])
