#!/usr/bin/env
import sys, getopt
import obtainstat
import multiprocessing as mp

def main(argv):
	path, L, outfile = readInput(argv)
	with open(path, 'r') as f:
		l = f.readline()
	l = l.split()
	data = [x[0] for x in l]
	output = mp.Queue()
	P, alph = obtainstat.calcProbs(data, L, output)
	P_cond = obtainstat.calcCondProbs(P, L, alph)
	H = obtainstat.calcCondEntropy(P, P_cond, L)
	obtainstat.saveAsStates(P_cond, alph, outfile)
	return

def readInput(argv):
	path = ""
	L = ""
	outfile = ""
	try:
		opts, args = getopt.getopt(argv, "hp:L:o:", ["ifile=", "L=", "ofile="])
	except getopt.GetoptError:
		print 'generateDataFromFile.py -p <inputfile> -L <algorithmL> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'generateDataFromFile.py -p <inputfile> -L <algorithmL> -o <outputfile>'
			sys.exit()
		elif opt in ("-p", "--ifile"):
			path = arg
		elif opt in ("-L", "--L"):
			L = int(arg)
		elif opt in ("-o", "--ofile"):
			outfile = arg
	return [path, L, outfile]

if __name__ == "__main__":
	main(sys.argv[1:])
