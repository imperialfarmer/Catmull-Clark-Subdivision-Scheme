#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This is the main file for computing subdivision surfaces.
	
Modules:
	geometry: construct mesh information, then pass 
	subdivision: process the geometric information from ``geometry``, then the mesh 
		will be updated using Catmull-Clark scheme.
	visualisation: post-process for the refined shpae. Result can be visualised using
		matplot or as a ouput model *.vtu output file.
	helper: provides auxilary functions for other modules

To use:
	Details can be seen in option `-h` or `--help`
	If test the file please type `test.py -p` to run subdivision for a 2d square, 
	or type `test.py -i 3d_example.dat -p` to run subdivision for a 3d square.
	Two test models (2d and 3d) are prepared, which are put in ``model``, also code 
	will look for model file in ``model`` folder.
	Nodes and edges can be seen by switch on `-p` or `--plot`

@author: Ge_Yin
"""

import sys, getopt, time

from geometry import Mesh as mesh
from subdivision import subdivision
import visualisation as view

def main(argv):
	"""Function to generate subdivision surfaces
	
	Agrs:
		The input will be passed to main function via `argv`:
		`-i <inputfile>` or `--infile=<inputfile>`: give input mesh file,
		`-o <outputfile> or -outfile=<outputfile>`: give directory to save result
		`-m <maxstep> or `--maxstep=<maxstep>`: give the number of iterations
		`-h` or `--help`: call help
		`-p` or `--plot`: option to plot points and edges"""
		
	
	inputfile = ""
	outputfile = ""
	maxstep = -1
	plot = False

	try:
		opts, args = getopt.getopt(argv, "hi:o:pm:" ,\
			["infile=", "outfile=", "maxstep=","help","plot"])
	except getopt.GetoptError:
		print('Error: please try test.py -i <inputfile> -o <outputfile> -m <maxstep>')
		print('   or: test.py --infile=<inputfile> --outfile=<outputfile> --maxstep=<maxstep>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print('\ntest.py -i <inputfile> -o <outputfile> -max <maxstep>')
			print('or: test.py --infile=<inputfile> --outfile=<outputfile> --maxstep=<maxst>')
			print('\nTo plot results: -p (matplotlib is needed for plotting)\n')
            
			sys.exit()

		elif opt in ("-i", "--infile"):
			inputfile = arg
			try:
				testfile = open('./model/' + inputfile, 'r')
			except IOError: 
				print('!Error: Could not read input file: ', inputfile)
				print("        Make sure the model file is in folder './model'\n")
				sys.exit()
			testfile.close()

		elif opt in ("-o", "--outfile"):
			outputfile = arg
			try:
				testfile = open(outputfile, 'r')
			except IOError: 
				print('!Error: Could not find output directory: ', outputfile)
				print("        Try './result' as file test output'\n")
				sys.exit()
			testfile.close()

		elif opt in ("-m", "--maxstep"):
			maxstep = int(arg)

		elif opt in("-p", "--plot"):
			plot = True
			
	missinginput = 0
	if not inputfile: 
		inputfile = '2d_example.dat'
		missinginput += 1
	if not outputfile:
		outputfile = 'result'
	if maxstep < 0: 
		maxstep = 3
		missinginput += 1
	
	if missinginput > 0: 
		print('\n!WARNING: ', missinginput, ' missing inputs, use defaults instead\n')

	print ('=== Input Inf.')
	print (' -> Input file:  ', inputfile)
	print (' -> Output file: ', outputfile)
	print (' -> Max Step:    ', maxstep)
	if plot: print(' -> Control point will be plotted after subdivision')

	inputfile = './model/' + inputfile
	outputfile = './' + outputfile

	#start subdivision process
	if maxstep > 0:
		for step in range(maxstep + 1):

			start_time = time.time()

			if step == 0: 
				print('\n=== Subdivision starts')
				model = mesh(inputfile)
			else: 
				subdivision(model)

			print("--- Iteration {0}    {1:8.2e}s".format(step, time.time() - start_time))
			view.write_VTUfile(model, outputfile + '/Step' + str(step) + '.vtu')

	else: 
		model = mesh(inputfile)
		print('\n=== No subdivision and original mesh will be saved')

	
	print('=== Subdivision finished\n')

	#if needed, plot control points
	if plot: 
		print('=== Wireframe is plotted in a seperate window\n')
		view.plot_frame(model)
		


if __name__ == '__main__':
	main(sys.argv[1:])
	

