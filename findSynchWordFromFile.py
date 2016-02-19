#!/usr/bin/env
import sys, getopt
import state
import graph
import probabilisticState
import probabilisticGraph as pg
import ptriestate as pts
import candidacytrie as ct
import findsynchwords as fsw

def main(argv):
	ifile, s, e, a, test, ofile = readInput(argv)
	print "Generating graph from graph file."
	testTree = pg.ProbabilisticGraph([],[])
	testTree.parseGraphFile(ifile)
	print "Generating synchronization words tree from graph."
	synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
	f = open(ofile, 'w')
	f.write("*********************************************\n")
	f.write("Input file: %s \n" %ifile)
	f.write("Statistical test: %s \n" %test)
	f.write("Confidence: %f \n" %a)
	f.write("*********************************************\n")
	print "Starting search for synch words."
	for w in range(s, e + 1):
	    r = fsw.findSynchWords(w, synchTrie, testTree, a, test)
	    if r:
		    f.write("Synchronization words found for window size %d:\n" %w)
		    for s in r:
			    f.write("%s\n" %s.name)
	    else:
		    f.write("No synchronization words found for window size: %d.\n" %w)
	    f.write("\n")
	    print "Found synch words for window size: %d" %w
	f.close()
	print "*************Found all synch words**************************"
	return

def readInput(argv):
	ifile = ""
	s = ""
	e = ""
	a = ""
	test = ""
	ofile = ""
	try:
		opts, args = getopt.getopt(argv, "hi:s:e:a:t:o:", ["ifile=", "startingwindowsize=", "endingwindowsize", "alpha", "testtype", "ofile="])
	except getopt.GetoptError:
		print 'findSynchWordFromFile.py -i <inputfile> -s <startingwindowsize> -e <endingwindowsize> -a <alpha> -t <testtype> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'findSynchWordFromFile.py -i <inputfile> -s <startingwindowsize> -e <endingwindowsize> -a <alpha> -t <testtype> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			ifile = arg
		elif opt in ("-s", "--startomgwindowsize"):
			s = int(arg)
		elif opt in ("-e", "--endingwindowsize"):
			e = int(arg)
		elif opt in ("-a", "--alpha"):
			a = float(arg)
		elif opt in ("-t", "--testtype"):
			test = arg
		elif opt in ("-o", "--ofile"):
			ofile = arg
	return [ifile, s, e, a, test, ofile]

if __name__ == "__main__":
	main(sys.argv[1:])
