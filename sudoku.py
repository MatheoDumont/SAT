from cnf_utils import cnf_variables, litteral

import copy
import random
import math
from itertools import combinations
"""
implementation pour representer un sudoku en une
formule propositionnelle


"""
global variables_sudoku
variables_sudoku = {}


def reset_var():
    variables_sudoku = {}


def var(row, column, value, s_size):
    var = (row * s_size + column) + (pow(s_size, 2) * value - 1)
    variables_sudoku[var] = (row, column, value)

    return var


def unvar(var):

    return variables_sudoku[var]


def printer(s, n):
    """
    Affichage pour sudoku
    """

    for i in range(pow(n, 2)):
        if i != 0 and i % n == 0:
            print('----------------------------')

        to_print = ''
        for j in range(pow(n, 2)):
            if j != 0 and j % n == 0:
                to_print += "|"

            to_print += " " + str(s[i][j]) + " "

        print(to_print)


def translate(s, dict_s):
    """
    Transforme le sudoku de depart en sudoku resolu a
    l'aide des assignations valide donnees dans dict_s
    """

    for key, val in dict_s.items():
        if val is True:
            row, col, val = unvar(key)
            s[row][col] = val

    return s


def display(s_start, dict_s, n):
    """
    Affichage du sudoku de depart, puis de sa version complete.
    """

    s_end = translate(copy.deepcopy(s_start), dict_s)

    print("############### Before ################\n")

    printer(s_start, n)
    print()

    print("############### After  ################\n")

    printer(s_end, n)
    print()


def sudoku():
    """
    Un sudoku de niveau simple
    """
    return [
        [0, 0, 9,   0, 0, 0,   0, 7, 1],
        [2, 0, 0,   6, 9, 8,   5, 0, 0],
        [6, 5, 0,   3, 1, 0,   0, 0, 2],

        [5, 6, 3,   8, 0, 1,   4, 0, 9],
        [0, 9, 0,   0, 0, 0,   0, 0, 8],
        [1, 0, 8,   9, 0, 2,   3, 6, 5],

        [7, 0, 5,   0, 8, 3,   2, 9, 0],
        [8, 3, 0,   0, 2, 0,   0, 5, 0],
        [9, 0, 0,   4, 6, 0,   0, 3, 7]
    ]


def formulate_sudoku(sudoku, n):
    """
    args:
        n: la taille d'un carre du sudoku, n^2 = le nombre de chiffre contenu, n*n*n= le nombre total de chiffre
        sudoku : list(list()) avec sudoku[i][j] = {x un nombre | 1 =< x =< n*n, '-' la case vide}

    return:
        list: une list de clause en 'forme normale conjonctive' ou CNF

    Pour construire le sudoku, 

    Contraintes:
        1) chaque case doit contenir au moins un nombre
        2) chaque ligne de taille n*n doit contenir qu'une seul fois un meme nombre
        3) chaque colonne de taille n*n doit contenir qu'une seul fois un meme nombre
        4) chaque carre de taille n*n doit contenir qu'une seul fois un meme nombre

    """
    reset_var()

    # Conjonctions de disjonctions
    clauses = []

    clause = []
    squared = n * n

    # Initialiser avec les nombres deja presents dans le sudoku
    for row in range(squared):
        for column in range(squared):
            if sudoku[row][column] != 0:
                clauses.append([
                    var(row, column, int(sudoku[row][column]), squared)
                ])

    # 1)
    for row in range(squared):
        for column in range(squared):
            clause = []
            for value in range(1, squared + 1):
                clause.append(var(row, column, value, squared))
            clauses.append(clause)

    # 2)
    """
                Pour chaque ligne on veut qu'il n'y ait pas deux fois le meme nombre
                donc on fait pour chaque valeur:
                i = row
                j = column
                v = value
    
                (xi,j,v nand xi,j+1,v) and (xi,j,v nand xi,j+2,v) and ... and (xi,j,v nand xi,j+(squared-i),v)
                De cette maniere on empeche deux case d'une meme ligne d'avoir le meme nombre

                x nand y <=> (not x or not y)
    """
    for row in range(squared):
        for column in range(squared):
            for value in range(1, squared + 1):
                for pair in range(column + 1, squared):
                    clauses.append([
                        litteral(var(row, column, value, squared), false=True),
                        litteral(var(row, pair, value, squared), false=True)
                    ])

    # 3)
    # Meme proceder pour les colonnes que pour les lignes
    for column in range(squared):
        for row in range(squared):
            for value in range(1, squared + 1):
                for pair in range(row + 1, squared):
                    clauses.append([
                        litteral(var(row, column, value, squared), false=True),
                        litteral(var(pair, column, value, squared), false=True)
                    ])

    # 4)
    # On fait en gros la meme chose mais en plus complique:
    """ 
    r = row
    c = column

        r   0     1     2 

    c     0 1 2 3 4 5 6 7 8 = r+i
       0 [-,-,-,-,-,-,-,-,-]
    0  1 [-,-,-,-,-,-,-,-,-]
       2 [-,-,-,-,-,-,-,-,-]
       3 [-,-,-,-,-,-,-,-,-]
    1  4 [-,-,-,-,-,-,-,-,-]
       5 [-,-,-,-,-,-,-,-,-]
       6 [-,-,-,-,-,-,-,-,-]
    2  7 [-,-,-,-,-,-,-,-,-]
       8 [-,-,-,-,-,-,-,-,-]
       = c+j
    """
    for y_case in range(0, squared, n):
        for x_case in range(0, squared, n):

            for i in range(n):
                for j in range(n):

                    for value in range(1, squared + 1):

                        for i_pair in range(i, n):
                            for j_pair in range(j, n):
                                # Pour ne pas avoir (not x or not x)
                                if j_pair == j:
                                    continue

                                clauses.append([
                                    litteral(
                                        var(y_case + i, x_case + j, value, squared), false=True),
                                    litteral(
                                        var(y_case + i_pair, x_case + j_pair, value, squared), false=True)
                                ])

    return clauses


def sudoku_generator(n, difficulty):
    """
    n: the size of the side of one square of the sudoku
    difficulty: number of filled case in each square(approximately)
    """

    squared = pow(n, 2)

    values = set(range(1, squared + 1))
    row = []
    column = []
    s = []

    # init du random generator
    random.seed()

    # a l'indice i se trouve la case i avec un set
    # avec un set representant les nombres present dans la case i
    square = []

    # contrainte pour les colonnes et lignes
    for i in range(squared):
        row.append(set())
        column.append(set())

    # contraintes pour les carres
    for i in range(squared):
        square.append(set())

    # init du sudoku avec des zeros
    for y in range(squared):
        l = []
        for x in range(squared):
            l.append(0)
        s.append(l)

    for diff in range(difficulty):
        for y in range(n):
            for x in range(n):

                # on genere un number non-present dans le square selectionne
                number = random.choice(
                    list(values - set(square[y * n + x])))

                # les rows ou n'est pas present number
                r_possible = set()
                for r in range(y * n, y * n + n):
                    if number not in row[r]:
                        r_possible.add(r)

                # les columns ou n'est pas present number
                c_possible = set()
                for c in range(x * n, x * n + n):
                    if number not in column[c]:
                        c_possible.add(c)

                possible_case = []

                # on test les cases possibles (celles vide)
                for r in r_possible:
                    for c in c_possible:
                        if s[r][c] == 0:
                            possible_case.append((r, c))

                if not possible_case:
                    continue

                r, c = random.choice(possible_case)

                s[r][c] = number
                column[c].add(number)
                row[r].add(number)
                square[y * n + x].add(number)

    return s
