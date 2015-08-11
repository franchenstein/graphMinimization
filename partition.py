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
        self.name = state.name
        self.outedges = state.outedges
        self.size = 0 if not state.name else 1
        
    def addToPartition(self, state):
        '''
        Input: state to be added to the partition
        Output: the current partition will now have a new state
        '''
        
        #Checks to see whether the state is already in the partition:
        if state.name not in self.name:
            #Adds the state's name to the partition, separated by comma:
            if not self.name:
                self.name = state.name
            else:
                self.name = self.name + "," + state.name
            #Adds each outedge of the added state to the partition's edges:
            for edge in state.outedges:
                if edge not in self.outedges:
                    self.outedges = self.outedges + [edge]
            self.size += 1           
            
    def updateEdges(self, partition):
        '''
        Input: partition to which the edges should be updated.
        Output: the current partition will have its outedges update accordingly.
        Description: When a partition has a new state added to it, all the 
        partitions that had that state in its outedges have to update the
        outedges in order to include the whole new partition at its destination
        state. 
        '''
        #Checks if the destination state is included in the input partition's 
        #name. If it is, outedges is updated: the destination state receives the
        #input partition's name.
        for i in range(0, len(self.outedges)):
            if self.outedges[i][1] in partition.name:
                edge = (self.outedges[i][0], partition.name)
                if edge not in self.outedges:
                    self.outedges[i] = edge
                else:
                    self.outedges.remove(self.outedges[i])
