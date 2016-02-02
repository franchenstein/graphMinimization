#!/usr/bin/env
import sys, getopt
import obtainstat
import multiprocessing as mp

def main(argv):
    shift, length, L, prob, outFile = readInput(argv)
    output = mp.Queue()
    data = obtainstat.generate(shift, length, prob)
    P, alph = obtainstat.calcProbs(data, L, output)
    P_cond = obtainstat.calcCondProbs(P, L, alph)
    H = obtainstat.calcCondEntropy(P, P_cond, L)
    obtainstat.saveAsStates(P_cond, alph, outFile)
    return
    
def readInput(argv):
    shift = ""
    length = ""
    L = ""
    prob = []
    outFile = ""
    try:
        opts, args = getopt.getopt(argv, "hs:l:L:p:o:", ["shift=","length=", "L=", "probfile=", "ofile="])
    except getopt.GetoptError:
        print 'generateData.py -s <shifttype> -l <sequencelength> -L <algorithmL> -p <probabilityfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'generateData.py -s <shifttype> -l <sequencelength> -L <algorithmL> -p <probabilityfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-s", "--shift"):
            shift = arg
        elif opt in ("-l", "--length"):
            length = int(arg)
        elif opt in ("-L", "--L"):
            L = int(arg)
        elif opt in ("-p", "--prob"):
            f = open(arg, 'r')
            for line in f:
                prob.append(float(line))
        elif opt in ("-o", "--ofile"):
            outFile = arg
    return [shift, length, L, prob, outFile]
        
if __name__ == "__main__":
    main(sys.argv[1:])   
