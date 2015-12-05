#!/usr/bin/env
import sys, getopt
import obtainstat
import multiprocessing as mp
import time

def main(argv):
    start_time = time.time()
    output = mp.Queue()
    path, L, s, outfile = readInput(argv)
    data = []
    f = open(path, 'r')
    for line in f:
    	for c in line:
    			if c != '\n':
    			    data.append(c)
	P, alph = obtainstat.calcProbsInParallel(data, L, s, output)
	P_cond = obtainstat.calcCondProbs(P, L, alph)
	H = obtainstat.calcCondEntropy(P, P_cond, L)
	obtainstat.saveAsStates(P_cond, alph, outfile)
    print  ("---- %s seconds ----" %(time.time() - start_time))
    return

def readInput(argv):
	path = ""
	L = ""
	outfile = ""
	try:
		opts, args = getopt.getopt(argv, "hp:L:s:o:", ["ifile=", "L=", "subprocesses=", "ofile="])
	except getopt.GetoptError:
		print 'generateDataFromFile.py -p <inputfile> -L <algorithmL> -s <subprocesses> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'generateDataFromFile.py -p <inputfile> -L <algorithmL> -s <subprocesses> -o <outputfile>'
			sys.exit()
		elif opt in ("-p", "--ifile"):
			path = arg
		elif opt in ("-L", "--L"):
			L = int(arg)
		elif opt in ("-s", "--subprocesses"):
			s = int(arg)
		elif opt in ("-o", "--ofile"):
			outfile = arg
	return [path, L, s, outfile]

if __name__ == "__main__":
	main(sys.argv[1:])
