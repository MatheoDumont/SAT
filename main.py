from utils import validate, variables
from CNF_utils import CNF_clauses, CNF_variables
from tree import *
from sudoku import sudoku, formulate_sudoku

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
    clauses = formulate_sudoku(sudoku(), 3)
    res = DPLL(clauses, CNF_variables(clauses))

    for key, value in res.items():
        if value is False:
            del res[key]

    print(res)
