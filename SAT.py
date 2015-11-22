########################################################################################################################
#
#   File name:      SAT.py
#   Authors:        Maciej Przydatek & Giliam Datema
#   Created:        15/11/2015
#
#   Course:         Artificial Intelligence & Decision Systems
#   Assignment:     2
#   Institution:    Instituto Superior Técnico Lisboa
#
########################################################################################################################

"""
This program reads SAT problems from input files in DIMACS format and uses three different algorithms for solving the
SAT problems: GSAT, WalkSAT and DPLL. The output files are also in DIMACS format.
"""

from functions import *
from time import clock
from os import listdir

# Set problems directory
problems_dir = '3SATproblems/'

# List all files in problems directory
files = listdir(problems_dir)

# Loop through all files
for file in files:
    # If file is 3SAT problem file in cnf format, solve the problem using GSAT WalkSAT and DPLL
    if file.endswith('.cnf'):
        print('Solving problem: '+file)
        filename = problems_dir+file

        # Get number of variables, number of clauses and the sentence
        N, C, sentence = readFile(filename)

        # # Run and time the GSAT algorithm and save results
        # print('Running GSAT')
        # t0 = clock()
        # GSAT_sol = GSAT(N,sentence,max_restarts=10,max_climbs=100)
        # t_GSAT = clock() - t0
        # writeFile(filename,'GSAT',N,C,GSAT_sol,t_GSAT)
        #
        # # Run and time the WalkSAT algorithm and save results
        # print('Running WalkSAT')
        # t0 = clock()
        # WalkSAT_sol = WalkSAT(N,sentence,p=0.5,max_flips=100)
        # t_WalkSAT = clock() - t0
        # writeFile(filename,'WalkSAT',N,C,WalkSAT_sol,t_WalkSAT)

        # Run and time the DPLL algorithm and save results
        # print('Running DPLL')
        # t0 = clock()
        DPLL_sol = DPLLInit(N, sentence)
        print("solved")
        break
        # t_DPLL = clock() - t0
        # writeFile(filename,'DPLL',N,C,DPLL_sol,t_DPLL)