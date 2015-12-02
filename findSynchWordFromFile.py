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
	ifile, w, ofile = readInput(argv)
	testTree = pg.ProbabilisticGraph([],[])
	testTree.parseGraphFile(ifile)
	synchTrie = ct.CandidacyTrie(testTree.states, testTree.alphabet)
	r = fsw.findSynchWords(w, synchTrie, testTree)
	f = open(ofile, 'w')
	f.write("*********************************************\n")
	f.write("Input file: %s \n" %ifile)
	f.write("Window size: %d \n" %w) 
	f.write("*********************************************\n")
	if r:
		f.write("Synchronization words found:\n")
		for s in r:
			f.write("%s\n" %s.name)
	else:
		f.write("No synchronization words found.\n")
	f.close()
	return

def readInput(argv):
	ifile = ""
	w = ""
	ofile = ""
	try:
		opts, args = getopt.getopt(argv, "hi:w:o:", ["ifile=", "windowsize=", "ofile="])
	except getopt.GetoptError:
		print 'findSynchWordFromFile.py -i <inputfile> -w <windowsize> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print 'findSynchWordFromFile.py -i <inputfile> -w <windowsize> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			ifile = arg
		elif opt in ("-w", "--windowsize"):
			w = int(arg)
		elif opt in ("-o", "--ofile"):
			ofile = arg
	return [ifile, w, ofile]

if __name__ == "__main__":
	main(sys.argv[1:])
