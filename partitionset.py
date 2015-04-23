import partition

class PartitionSet:
    
    def __init__(self, partitions):
        self.partitions = partitions
        
    def updatePartitionsEdges(self):
        for partToUpdate in self.partitions:
            for otherParts in self.partitions:
                partToUpdate.updateEdges(otherParts)
        
