from state import State

class Partition(State):
    '''
    A partition is a state created by merging states together after it is
    computed they represent an equivalent state. It has the same attributes as
    the class State, but it includes functions that add new states to the
    partition and that updates its outedges to the names of another partition
    of the same partition set.
    '''

    def __init__(self, state):
        #A new partition is initialized with just one state:
        State.__init__(self, state.name, state.outedges)
        
    def addToPartition(self, state):
        '''
        Input: state to be added to the partition
        Output: the current partition will now have a new state
        '''
        
        #Checks to see whether the state is already in the partition:
        if state.name not in self.name:
            #Adds the state's name to the partition, separated by comma:
            self.name = self.name + "," + state.name
            #Adds each outedge of the added state to the partition's edges:
            for edge in state.outedges:
                self.outedges.append(edge)
            
    def updateEdges(self, partition):
        '''
        Input: partition to which the edges should be updated.
        Output: the current partition will have its outedges update accordingly.
        Description: When a partition has a new state added to it, all the 
        partitions that had that state in its outedges have to update the
        outedges in order to include the whole new partition at its destination
        state. 
        '''
    
        i = 0
        for edge in self.outedges:
            #Checks if the destination state is included in the input
            #partition's name.
            if edge[1] in partition.name:
                #If it is, outedges is updated: the destination state receives
                #the input partition's name.
                self.outedges[i] = (edge[0], partition.name)
            i = i +1
