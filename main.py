from utils import validate
from CNF_utils import CNF_clauses, CNF_variables
from tree import *

import time


if __name__ == '__main__':
    prop = "x or not y"
    litts = validate(prop)

    prop2 = "x and ( not y or z )"
    litts2 = validate(prop2)

    print(recursive_tree(litts, prop))

    print(fifo(litts2, prop2))
    print(recursive_tree(litts2, prop2))

    cnf = "(x or y) and ( z or w) and (not x or w)"
    CNF = CNF_clauses(cnf)
    variabs = CNF_variables(CNF)


    print(cnf)
    print(CNF)
    print(variabs)

    print("recursive_tree")
    t = time.time()
    recursive_tree(variabs, cnf)
    print(time.time() - t)

    print("fifo")
    t = time.time()
    fifo(variabs, cnf)
    print(time.time() - t)

    print("DPLL")
    t = time.time()
    print(DPLL(CNF, variabs))
    print(time.time() - t)
