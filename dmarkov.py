import probabilisticGraph as pg
import probabilisticState as ps

class DMarkov(pg.ProbabilisticGraph):
    def __init__(self, g, D):
        s = [x for x in g.states if len(x.name) == D]
        states = []
        for x in s:
            n = x.name
            outedges = []
            for a in g.alphabet:
                m = n[1:len(n)] + a
                for e in x.outedges:
                    if e[0] == a:
                        p = e[2]
                outedges.append((a, m, p))
            states.append(ps.ProbabilisticState(n, outedges))
        pg.ProbabilisticGraph.__init__(self, states, g.alphabet)
    
