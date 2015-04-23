#!/usr/bin/env

import state
import partition
import graph
import partitionset

g = graph.Graph([], [])
g.parseGraphFile("reducedgraph.txt")

p1 = partition.Partition(state.State('', []))
p1.addToPartition(g.states[0])
p1.addToPartition(g.states[2])
p1.addToPartition(g.states[4])

p2 = partition.Partition(g.states[1])
for i in [3, 5]:
    p2.addToPartition(g.states[i])

P = partitionset.PartitionSet([p1, p2])
P.updatePartitionsEdges()
