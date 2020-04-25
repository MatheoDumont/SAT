from utils import validate, variables
from cnf_utils import cnf_from_str, cnf_variables
from dpll_solver import DPLL
from sudoku import *
import numpy as np
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
    s = generate_glouton_with_verification(3)
    t = time.time() - t
    print(f'Time for // size=3 // is {t} ')
    printer(s, 3)

    t = time.time()
    s = generate_glouton_with_verification(4)
    t = time.time() - t
    print(f'Time for // size=4 // is {t} ')
    printer(s, 4)

    t = time.time()
    s = generate_glouton_with_verification(5)
    t = time.time() - t
    print(f'Time for // size=5 // is {t} ')
    printer(s, 5)


def bench_sudoku_resolution():
    # timeit.timeit("single_test", globals=locals())
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


def single_test():
    s = sudoku()

    clauses = formulate_sudoku(s, 3)

    sol = DPLL(clauses)
    
    display(s, sol, 3)

def bigger_single_test():
    s = s_16()

    clauses = formulate_sudoku(s, 4)

    sol = DPLL(clauses)
    
    display(s, sol, 4)


def get_working_test(n):
    t = time.time()
    sudoku = []
    working = False

    while not working:
        sudoku = generate_glouton_with_verification(n)

        clauses = formulate_sudoku(sudoku, n)
        sol = DPLL(clauses)
        if sol:
            working = True
        else:
            print("not working")

    print(f'Time to generate SAT sudoku // size={n} // is {time.time() - t} ')
    display(sudoku, sol, n)

    return sudoku


def debug():
    clauses = []
    n = 2
    squared = n**2

    for row in range(0, squared, n):
        for col in range(0, squared, n):

            for row_case in range(row, row + n):
                for col_case in range(col, col + n):

                    for row_case_pair in range(row_case, row+n):
                        start = col_case+1 if row_case == row_case_pair else 0
                        for col_case_pair in range(start, col+n):

                            for value in range(1, squared+1):
                                clauses.append([
                                    (row_case, col_case, value, False),
                                    (row_case_pair, col_case_pair, value, False)
                                    # litteral(
                                    #     var(row_case, col_case, value, squared), false=True),
                                    # litteral(
                                    #     var(row_case_pair, col_case_pair, value, squared), false=True)
                                ])


if __name__ == '__main__':
    bigger_single_test()
