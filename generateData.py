#!/usr/bin/env
import sys, getopt
import obtainstat

def main(argv):
    shift, length, L, prob, outFile = readInput(argv)
    data = obtainstat.generate(shift, length, prob)
    P, alph = obtainstat.calcProbs(data, L)
    P_cond = obtainstat.calcCondProbs(P, L, alph)
    obtainstat.saveAsStates(P_cond, alph, outFile)
    return
    
def readInput(argv):
    shift = ""
    length = ""
    L = ""
    prob = [0.0, 0.0, 0.0]
    outFile = ""
    try:
        opts, args = getopt.getopt(argv, "hs:l:L:p:q:r:o:", ["shift=","length=", "L=", "prob0=", "prob1=", "prob2=", "ofile="])
    except getopt.GetoptError:
        print 'generateData.py -s <shifttype> -l <sequencelength> -L <algorithmL> -p <transitionprobability> -q <transitionprobability> -r <transitionprobability> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'generateData.py -s <shifttype> -l <sequencelength> -L <algorithmL> -p <transitionprobability> -q <transitionprobability> -r <transitionprobability> -o <outputfile>'
            sys.exit()
        elif opt in ("-s", "--shift"):
            shift = arg
        elif opt in ("-l", "--length"):
            length = int(arg)
        elif opt in ("-L", "--L"):
            L = int(arg)
        elif opt in ("-p", "--prob0"):
            prob[0] = float(arg)
        elif opt in ("-q", "--prob1"):
            prob[1] = float(arg)        
        elif opt in ("-r", "--prob2"):
            prob[2] = float(arg)
        elif opt in ("-o", "--ofile"):
            outFile = arg
    return [shift, length, L, prob, outFile]
        
if __name__ == "__main__":
    main(sys.argv[1:])   
