from utils import validate, variables
from cnf_utils import cnf_from_str, cnf_variables
from tree import *
from sudoku import sudoku, formulate_sudoku, display
import sudoku as s

import time


def assertion():
    prop = "x or not y"
    litts = validate(prop)

    prop2 = "x and ( not y or z )"
    litts2 = validate(prop2)

    print(recursive_tree(litts, prop))

    print(fifo(litts2, prop2))
    print(recursive_tree(litts2, prop2))

    cnf = "(x or y) and ( z or w) and (not x or w)"
    CNF = CNF_clauses(cnf)
    set_variabs = CNF_variables(CNF)

    print(cnf)
    print(CNF)
    print(set_variabs)

    print("recursive_tree")
    t = time.time()
    recursive_tree(list(set_variabs), cnf)
    print(time.time() - t)

    print("fifo")
    t = time.time()
    fifo(list(set_variabs), cnf)
    print(time.time() - t)

    print("DPLL")
    t = time.time()
    print(DPLL(CNF, set_variabs))
    print(time.time() - t)


if __name__ == '__main__':
    n = 3

    clauses = formulate_sudoku(sudoku(), n)
    t = time.time()
    res = DPLL(clauses, cnf_variables(clauses))

    print(time.time() - t)
    s.display(sudoku(), res, n)
