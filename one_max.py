#!/usr/bin/env python3
#######################################################################################
#
#	Copyright (c) 2021, Wiphoo (Terng) Methachawalit, All rights reserved.
#
#######################################################################################


#######################################################################################
#
#	STANDARD IMPORTS
#

import sys

from optparse import OptionParser

import random

import logging

#######################################################################################
#
#	LOCAL IMPORTS
#


#######################################################################################
#
#	PROGRAM DEFENITIONS
#

#	version of this program
Version = '0.1'

#	program usage, it is a string of an example for how to use this program with arugments
ArgsUsage = '<NUM_BTS>'

#	number of required arugments
NumRequiredArgs = 1

#######################################################################################
#
#	GLOBAL VARIABLES
#


#######################################################################################
#
#	HELPER FUNCTIONS
#


#######################################################################################
#
#	CLASS DEFINITIONS
#

class OneMaxCompactGeneticSolver(object):

	def __init__(self, num_bits, 
					population_size=None):
		self._num_bits = num_bits
		self._population_size = 100 if population_size is None else population_size

		#	probability vector [0,1] probability to be 1 in candidate
		self._probabilities = None

		#	candidate
		self._candidate = None

		#	iteration
		self._iteration = None
		self._num_function_evaluation = None

		#	initialize
		self._initialize()

	def _initialize(self):
		""" initialize probability vector and cnadidate """
		
		#	initailize the probability to be 0.5 [0,1]
		self._probabilities = [0.5 for i in range(self._num_bits)]

		#	random create a candidate
		self._candidate = [random.randint(0, 1) for i in range(self._num_bits)]

		#	intiialize to be 0
		self._iteration = 0
		self._num_function_evaluation = 0

	def _do_generation_iteration(self):
		""" do a generation iteration """
		
		#	generate new candidates
		#		first candidate
		first_candidate = [random.choices([0,1], weights=[1-probability, probability])[0] for probability in self._probabilities]
		#		second candidate
		second_candidate = [random.choices([0,1], weights=[1-probability, probability])[0] for probability in self._probabilities]

		#	do a fitnesss comparison 
		first_candidate_fitness = self._fitness(first_candidate)
		second_candidate_fitness = self._fitness(second_candidate)
		
		logging.debug(f'iteration[{self._iteration}]\n      - first candiate {first_candidate_fitness} - {first_candidate}\n      - second candidate {second_candidate_fitness} - {second_candidate}')

		#	ignore
		if first_candidate_fitness == second_candidate_fitness:
		#	skip, no winner in this iteration
			logging.debug(f'[{self._iteration}] - NO winner in this iteration')
			self._iteration += 1
			return

		#	found winner
		winner_candidate, loser_candidate = (first_candidate, second_candidate) \
												 if first_candidate_fitness > second_candidate_fitness \
													else (second_candidate, first_candidate)

		logging.debug(f'iteration[{self._iteration}]\n      - winner fitness {self._fitness(winner_candidate)} - {winner_candidate}\n      - loser fitness {self._fitness(loser_candidate)} - {loser_candidate}')

		#	update the probability vector
		for index, (winner_bit, loser_bit) in enumerate(zip(winner_candidate, loser_candidate)):
			if winner_bit == 1 and loser_bit == 0:
				# do update probability vector at this bit direct to 1
				if self._probabilities[index] + 1 / self._population_size <= 1.0:
					self._probabilities[index] += 1 / self._population_size
			elif winner_bit == 0:
				# do update probability vector at this bit direct to 0
				if self._probabilities[index] - 1 / self._population_size >= 0:
					self._probabilities[index] -= 1 / self._population_size
		
		#	update new candidate
		self._candidate = winner_candidate

		#	done
		logging.debug(f'DONE - iteration[{self._iteration}] - {self._probabilities}')

		#	increase iteraiton count
		self._iteration += 1
		self._num_function_evaluation += 1

	def _fitness(self, candidate):
		""" fitness function """
		fitness = candidate.count(1)
		logging.debug(f'fitness = {fitness} of {candidate}')
		return fitness

	def run(self):
		""" run the compact genetic algorithm """

		#	loop until the solution is found
		while self._fitness(self._candidate) != self._num_bits:
			#	do generation iteration
			self._do_generation_iteration()

		logging.debug(f'number of iteration = {self._iteration}')
		logging.debug(f'number of evaluation function = {self._num_function_evaluation}')


#######################################################################################
#
#	MAIN
#


def main():
	''' main function of this program '''
	
	###################################################################################
	#	options parsing

	usage = 'usage: %prog [options] {!r}'.format( ArgsUsage )
	parser = OptionParser( usage=usage, version=Version )
	parser.add_option( '-v', '--verbose',
							action='store_true', dest='verbose', default=True )
	( options, args ) = parser.parse_args()
	
	#	check the required arguments
	if len( args ) != NumRequiredArgs:
	#	the given arguments is not equals the required arguments,
	#		so print the error meessage and exit
		parser.error( 'incorrect number of arguments.' )
		sys.exit( -1 )
	
	###################################################################################
	#	parse arguments / options
	
	num_bits = int(args[0])
	
	###################################################################################
	#	main
	logging.getLogger().setLevel(logging.DEBUG)
	logging.debug(f'compact genetic algorithm for {num_bits} bits')

	# solve
	one_max_solver = OneMaxCompactGeneticSolver(num_bits)
	one_max_solver.run()

if __name__ == "__main__":
	#	call main function
	main()

