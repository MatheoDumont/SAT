from utils import validate, variables
from cnf_utils import cnf_from_str, cnf_variables
from dpll_solver import DPLL
from sudoku import sudoku, formulate_sudoku, printer, display, generate

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


def bench_s_gen():
    print(f'BENCHMARK SUDOKU GENERATOR WITH DIFFICULTY = 4')

    t = time.time()
    s = generate(3, 4)
    t = time.time() - t
    print(f'Time for // size=3 // is {t} ')
    printer(s, 3)

    t = time.time()
    s = generate(4, 7)
    t = time.time() - t
    print(f'Time for // size=4 // is {t} ')
    printer(s, 4)

    t = time.time()
    s = generate(5, 10)
    t = time.time() - t
    print(f'Time for // size=5 // is {t} ')
    printer(s, 5)


def bench_sudoku_resolution():
    clauses = formulate_sudoku(sudoku(), 3)

    t = time.time()

    assert DPLL(clauses) is not False
    print(f'Temps pour resoudre un sdk de // taille=3 // is {time.time() - t}')

    s = generate(4, 4)
    clauses = formulate_sudoku(s, 4)

    t = time.time()
    assert DPLL(clauses) is not False
    print(f'Temps pour resoudre un sdk de // taille=4 // is {time.time() - t}')

    s = generate(5, 4)
    clauses = formulate_sudoku(s, 5)

    t = time.time()
    assert DPLL(clauses) is not False
    print(f'Temps pour resoudre un sdk de // taille=5 // is {time.time() - t}')


if __name__ == '__main__':
    bench_sudoku_resolution()
