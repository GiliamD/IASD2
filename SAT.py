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
import matplotlib.pyplot as plt
from statistics import mean

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

        # If no GSAT ouput exists yet for this problem, perform GSAT
        if not files.count(file.replace('.cnf','.solGSAT')):
            # Run and time the GSAT algorithm and save results
            print('Running GSAT')
            t0 = clock()
            GSAT_sol = GSAT(N,sentence,max_restarts=20,max_climbs=5*N)
            t_GSAT = clock() - t0
            writeFile(filename,'GSAT',N,C,GSAT_sol,t_GSAT)

        # If no WalkSAT ouput exists yet for this problem, perform WalkSAT
        if not files.count(file.replace('.cnf','.solWalkSAT')):
            # Run and time the WalkSAT algorithm and save results
            print('Running WalkSAT')
            t0 = clock()
            WalkSAT_sol = WalkSAT(N,sentence,p=0.5,max_flips=200*N)
            t_WalkSAT = clock() - t0
            writeFile(filename,'WalkSAT',N,C,WalkSAT_sol,t_WalkSAT)

        # # If no DPLL ouput exists yet for this problem, perform DPLL
        # if not files.count(file.replace('.cnf','.solDPLL')):
        #     # Run and time the DPLL algorithm and save results
        #     print('Running DPLL')
        #     t0 = clock()
        #     DPLL_sol = DPLLInit(N, sentence)
        #     t_DPLL = clock() - t0
        #     writeFile(filename,'DPLL',N,C,DPLL_sol,t_DPLL)

        else:
            print('Output files already exist.')


# # Initialize dictionaries to store number of variables N, number of clauses C and execution time T for each problem
# GSATdata = dict()
# WalkSATdata = dict()
# DPLLdata = dict()
#
# # Read output files and collect ratio C/N and corresponding execution time T
# for file in files:
#     if file.endswith('.solGSAT'):
#         N,C,T = readSolFile(problems_dir+file)
#         if C/N in GSATdata.keys():
#             GSATdata[C/N] = GSATdata[C/N].append(T)
#         else:
#             GSATdata[C/N] = [T]
#     elif file.endswith('.solWalkSAT'):
#         N,C,T = readSolFile(problems_dir+file)
#         if C/N in WalkSATdata.keys():
#             WalkSATdata[C/N] = WalkSATdata[C/N].append(T)
#         else:
#             WalkSATdata[C/N] = [T]
#     elif file.endswith('.solDPLL'):
#         N,C,T = readSolFile(problems_dir+file)
#         if C/N in DPLLdata.keys():
#             DPLLdata[C/N] = DPLLdata[C/N].append(T)
#         else:
#             DPLLdata[C/N] = [T]
#     else:
#         continue

# # Plot results
# plt.figure(1)
# x = list(zip(*sorted(GSATdata.items())))[0]
# y = list(zip(*sorted(GSATdata.items())))[1]
# plt.plot(x,y,'ok-')
#
# x = list(zip(*sorted(WalkSATdata.items())))[0]
# y = list(zip(*sorted(WalkSATdata.items())))[1]
# plt.plot(x,y,'sr--')
#
# plt.show()

print('Done.')