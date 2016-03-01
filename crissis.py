import state
import graph
import probabilisticState
import probabilisticGraph as pg

def crissis(synchWordState, tree, alpha, testType):
    q = [synchWordState]
    qTild = []
    for child in synchWordState.obtainChildren(tree):
        qTild.append(child)
    
    while True:
        if qTild:
            w = qTild.pop(0)
            wStar = matchState(w, q, 1, tree, alpha, testType)
            if wStar is None:
                q.append(w)
                for child in w.obtainChildren(tree):
                    qTild.append(child)
            else:
                for state in q:
                    for edge in state.outedges:
                        if edge[1] == w.name:
                            newedge = (edge[0], wStar.name, edge[2])
                            state.outedges.remove(edge)
                            state.outedges.append(newedge)
        else:
            break
    finalGraph = pg.ProbabilisticGraph(q,tree.alphabet)
    return finalGraph
    
def matchState(w, q, L2, tree, alpha, testType):
    for i in q:
        p = tree.compareMorphs(w.outedges, i.outedges, alpha, testType)
        if p[0]:
            return i
    return None
