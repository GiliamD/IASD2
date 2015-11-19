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

# from classes import *
from functions import *

from os import listdir

# Set problems directory
problems_dir = '3SATproblems/'

# Get all files in problems directory
files = listdir(problems_dir)

N, C, sentence = readFile(problems_dir+files[0])

GSAT_sol = GSAT(N,sentence,max_restarts=10,max_climbs=100)
