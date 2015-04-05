from state import State

class Graph:
    
    def __init__(self, states, alphabet):
        self.states = states
        self.alphabet = alphabet
   
    def parseGraphFile(self, filePath):
        with open(filePath) as f:
            lines = f.readlines()
            
        i = 0
        outedges = []
        stateList = []
        alph = []
        name = ''
        
        for line in lines:
            
            if line == "\n":
                i = 0
                
                stateList.append(State(name, outedges))
                name = ''
                outedges = []
                
            else:
            
                if i == 0:
                    j = 0                 
                    i = i + 1   
                    
                    while line[j] != '\n':
                        name = name + line[j]
                        j = j + 1
                
                else:            
                    j = 0
                    edge = ''
                    stateName = ''
                   
                    while line[j] != ' ':
                        edge = edge + line[j]
                        j = j + 1
                    
                    if edge not in alph:
                        alph.append(edge)
                    
                    k = j + 1
                        
                    while line[k] != '\n':
                        stateName = stateName + line[k]
                        k = k + 1
                        
                    outedges.append((edge, stateName))
                
        self.states = stateList        
        self.alphabet = alph
        
    def saveGraphFile(self, filePath):
        
        f = open(filePath, 'w')
        lines = []
        
        for s in self.states:
            lines.append(s.name + '\n')
            for e in s.outedges:
                lines.append(e[0] + ' ' + e[1] + '\n')
            lines.append('\n')
            
        f.writelines(lines)
        f.close
