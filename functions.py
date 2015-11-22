########################################################################################################################
#
#   File name:      functions.py
#   Authors:        Maciej Przydatek & Giliam Datema
#   Created:        15/11/2015
#
#   Course:         Artificial Intelligence & Decision Systems
#   Assignment:     2
#   Institution:    Instituto Superior Técnico Lisboa
#
########################################################################################################################

"""
This file contains the function definitions of the functions used in SAT.py, notably the three algorithms for solving
SAT problems: GSAT, WalkSAT and DPLL.
"""

from random import choice
from copy import deepcopy
from numpy.random import choice as pchoice


def readFile(filename):
    """
    Reads and processes 3SAT problem input file of DIMACS format and returns #variables, #clauses and the clauses. Input
    file format is assumed to be cnf.

    :param filename: file name string
    :return N: number of variables
    :return C: number of clauses
    :return clauses: list of clauses
    """

    # Open file for reading. NOTE: Use of 'with' does not require close()
    with open(filename, 'r') as file:
        # Initialize list of clauses, i.e. the sentence
        clauses = []
        for line in file:
            # Skip comment lines starting with 'c'
            if not line.startswith('c'):
                # Read property line starting with 'p'. Convert number of variables and clauses from string to integer.
                # Format is assumed to be always cnf, hence does not need to be read
                if line.startswith('p'):
                    N = int(line.split()[-2])   # number of variables
                    C = int(line.split()[-1])   # number of clauses
                # Convert literals from string to integer and append clause to list (after removing the trailing zero)
                else:
                    clauses.append(list(map(int,line.split()[0:-1])))

    return N, C, clauses


def writeFile(filename, N, C, V, T):
    """
    Writes solution to output file in DIMACS format, containing the number of variables and clauses, the variable
    assignments and the timing of the code execution.

    :param filename: file name string
    :param N: number of variables
    :param C: number of clauses
    :param V: variable assignments
    :param T:
    :return:
    """

    # Create output file with same name as input file, but with extension .sol
    with open(filename.replace('.cnf','.sol'),'w') as file:
        file.write('c '+'Solution to 3SAT problem defined in '+filename.replace('3SATproblems/','')+'\n')
        # If there is a solution, output 1 (= satisfiable)
        if isinstance(V,list):
            solution = 1
        # If no solution was found, output 0 (= unsatisfiable) in case of DPLL or -1 (= no decision) in case of GSAT or
        # WalkSAT
        else:
            solution = V
        # Write solution line
        file.write('s '+'cnf '+str(solution)+' '+str(N)+' '+str(C)+'\n')
        # Write timing line, including repetition of solution line
        file.write('t '+'cnf '+str(solution)+' '+str(N)+' '+str(C)+' '+str(T)+'\n')
        # Write variable lines
        for i in range(0,len(V)):
            if V[i] is not False:
                file.write('v '+str(i+1)+'\n')
            else:
                file.write('v '+str(-(i+1))+'\n')

    return 1


def randAssignment(N):
    """
    Generates random truth assignment for the N variables, i.e. a model.

    :param N: number of variables
    :return model: list of (boolean) truth assignments for all variables
    """

    model = [choice([False,True]) for i in range(1,N+1)]

    return model


def assign(model, sentence):
    """
    Assigns variable values from model to sentence.

    :param model: list of (boolean) truth assignments ordered by variable number
    :param sentence: list of clauses with literals represented by positive or negative integers
    :return tmp_sentence: list of clauses with literals evaluated as True/False
    """

    # Create copy of model and sentence without reference
    tmp_model = model[:]
    tmp_sentence = deepcopy(sentence)

    # Loop through clauses of sentence
    for i in range(len(tmp_sentence)):
        # Loop through the three literals of clause
        for j in range(3):
            literal = sentence[i][j]
            # If literal is positive, substitute literal by truth assignment
            if literal > 0:
                tmp_sentence[i][j] = tmp_model[literal-1]
            # If literal is negative, substitute literal by negation of truth assignment
            else:
                tmp_sentence[i][j] = not tmp_model[abs(literal)-1]

    return tmp_sentence


def satisfies(model, sentence):
    """
    Checks if a model satisfies all clauses of a sentence.

    :param model: list of (boolean) truth assignments ordered by variable number
    :param sentence: list of clauses with literals represented by positive or negative integers
    :return: True if model satisfies sentence, False otherwise
    """

    # Assign True/False to the variables in the sentence according to the model
    tmp_sentence = assign(model,sentence)

    # If there is any clause with all literals False, then sentence is unsatisfiable
    for clause in tmp_sentence:
        if all(literal is False for literal in clause):
            return False

    # If all clauses contain at least one literal that is True, the sentence is satisfiable
    return True


def numSatisfiedClauses(model, sentence):
    """
    Counts the number of clauses satisfied by the model.

    :param model: list of (boolean) truth assignments ordered by variable number
    :param sentence: list of clauses with literals represented by positive or negative integers
    :return countSatisfiedClauses: number of clauses satisfied by the model
    """

    # Assign True/False to the variables in the sentence according to the model
    tmp_sentence = assign(model,sentence)

    # Count the number of satsfied clauses, i.e. clauses with at least one True literal
    countSatisfiedClauses = 0
    for clause in tmp_sentence:
        if not all(literal is False for literal in clause):
            countSatisfiedClauses += 1

    return countSatisfiedClauses


def randBestSuccessor(model, sentence):
    """
    Determines random best successor of the current model by flipping the variable assignments one by one and checking
    which variable flip results in the model with the highest number of satisfied clauses.

    :param model: list of (boolean) truth assignments ordered by variable number
    :param sentence: list of clauses with literals represented by positive or negative integers
    :return successor_model: random best successor of input model, i.e. copy with one flipped (boolean) truth assignment
    """

    # Create copy of sentence without reference
    tmp_sentence = deepcopy(sentence)

    # Create dictionary for storing the number of satisfied clauses for each successor
    satisfiedClauses = dict()

    # Initialize successor model as copy of model
    successor_model = model[:]

    # Loop through the variables
    for variable in range(1,len(model)+1):
        # Create copy of model without reference
        tmp_model = model[:]

        # Flip truth assignment for this variable. NOTE: -1 because index starts at 0 while variables start at 1
        tmp_model[variable-1] = not tmp_model[variable-1]

        # Count number of satisfied clauses for this successor and store in dictionary
        satisfiedClauses[variable] = numSatisfiedClauses(tmp_model,tmp_sentence)

    # Find successor with maximum number of satisfied clauses

    # Get keys (i.e. variables) corresponding to best successors when flipped. NOTE: max is assigned to variable m such
    # that it is only computed once
    bestVars = [key for m in [max(satisfiedClauses.values())] for key,val in satisfiedClauses.items() if val == m]

    # If multiple best successors, choose one randomly
    randBestVar = choice(bestVars)

    # Flip the variable in the model. NOTE: Again -1, because variables start at 1 and index at 0
    successor_model[randBestVar-1] = not model[randBestVar-1]

    # Return random best successor model
    return successor_model


def randBestSuccessor2(clause, model, sentence):
    """
    Determines random best successor of the current model by flipping the variable assignments of the variables in the
    specified clause one by one and checking which variable flip results in the model with the highest number of
    satisfied clauses. NOTE: The difference with randBestSuccessor() is that it only checks the variables present in the
    specified clause and not all variables of the model.

    :param clause: list of three literals
    :param model: list of (boolean) truth assignments ordered by variable number
    :param sentence: list of clauses with literals represented by positive or negative integers
    :return successor_model: random best successor of input model, i.e. copy with one flipped (boolean) truth assignment
    """

    # Create copy of sentence without reference
    tmp_sentence = deepcopy(sentence)

    # Create dictionary for storing the number of satisfied clauses for each successor
    satisfiedClauses = dict()

    # Initialize successor model as copy of model
    successor_model = model[:]

    # Loop through the variables in the clause
    for variable in list(map(abs,clause)):
        # Create copy of model without reference
        tmp_model = model[:]

        # Flip truth assignment for this variable. NOTE: -1 because index starts at 0 while variables start at 1
        tmp_model[variable-1] = not tmp_model[variable-1]

        # Count number of satisfied clauses for this successor and store in dictionary
        satisfiedClauses[variable] = numSatisfiedClauses(tmp_model,tmp_sentence)

    # Find successor with maximum number of satisfied clauses

    # Get keys (i.e. variables) corresponding to best successors when flipped. NOTE: max is assigned to variable m such
    # that it is only computed once
    bestVars = [key for m in [max(satisfiedClauses.values())] for key,val in satisfiedClauses.items() if val == m]

    # If multiple best successors, choose one randomly
    randBestVar = choice(bestVars)

    # Flip the variable in the model. NOTE: Again -1, because variables start at 1 and index at 0
    successor_model[randBestVar-1] = not model[randBestVar-1]

    # Return random best successor model
    return successor_model


def randFalseClause(model, sentence):
    """
    Returns a random choice of one of the clauses in the sentence that is not satisfied, i.e. that is False.

    :param model: list of (boolean) truth assignments ordered by variable number
    :param sentence: list of clauses with literals represented by positive or negative integers
    :return randomFalseClause: random choice of one of the clauses of the sentence that is False
    """

    # Assign True/False to the variables in the sentence according to the model
    tmp_sentence = assign(model,sentence)

    # List all False clauses in unassigned form, i.e. with the original literals/symbols instead of True/False
    falseClauses = []
    for i in range(len(tmp_sentence)):
        if all(literal is False for literal in tmp_sentence[i]):
            falseClauses.append(sentence[i])

    # Choose one of the False clauses randomly
    randomFalseClause = choice(falseClauses)

    return randomFalseClause


def GSAT(N, sentence, max_restarts, max_climbs):
    """
    GSAT algorithm. This random-restart, hill-climbing search algorithm returns a truth assignment that satisfies the
    sentence or returns False if no solution was found within the maximum number of restarts and climbs.

    :param N: number of variables
    :param sentence: list of clauses with literals represented by positive or negative integers
    :param max_restarts: max. number of restarts, i.e. random truth assignments / models
    :param max_climbs: max. number of climbs, i.e. variable flips / successors
    :return model: model satisfying the sentence, i.e. list of (boolean) truth assignments ordered by variable number
    :return: -1 if no solution found within max_climbs and max_restarts
    """

    for i in range(1,max_restarts+1):
        print('restart '+str(i))
        model = randAssignment(N)
        for j in range(1,max_climbs+1):
            print('climb '+str(j))
            if satisfies(model,sentence):
                return model
            else:
                model = randBestSuccessor(model,sentence)

    # Return -1 if failed to find a model that satisfies the sentence
    return -1


def WalkSAT(N, sentence, p, max_flips):
    """
    WalkSAT algorithm. This local-search algorithm returns a truth assignment that satisfies the sentence or returns
    False if no solution was found within the maximum number of flips.

    :param N: number of variables
    :param sentence: list of clauses with literals represented by positive or negative integers
    :param p: probability of performing a random variable flip rather than a greedy variable flip
    :param max_flips: maximum number of variable flips before giving up
    :return model: model satisfying the sentence, i.e. list of (boolean) truth assignments ordered by variable number
    :return: -1 if no solution found within max_flips
    """

    model = randAssignment(N)

    for i in range(1,max_flips+1):
        if satisfies(model,sentence):
            return model
        else:
            # Randomly choose False clause
            clause = randFalseClause(model,sentence)

            # With probability p, flip variable in model randomly chosen from clause
            if pchoice([True,False],p=[p,1-p]):
                # Randomly choose variable from clause
                variable = abs(choice(clause))
                # Flip variable truth assignment in model
                model[variable-1] = not model[variable-1]

            # Else, flip variable in model chosen from clause that maximizes the number of satisfied clauses
            else:
                model = randBestSuccessor2(clause,model,sentence)

    # Return -1 if failed to find a model that satisfies the sentence
    return -1


def DPLL(input):
    """
    DPLL algorithm.

    :param input:
    :return:
    """

    # Return 0 if failed to find a model that satisfies the sentence
    return 0