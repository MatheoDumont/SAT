from tree import DPLL
from CNF_utils import CNF_variables
"""
implementation pour representer un sudoku en une
formule propositionnelle


"""


def sudoku():
    """
    Un sudoku de niveau simple
    """
    return [
        ['-', '-', '9', '-', '-', '-', '-', '7', '1'],
        ['2', '-', '-', '6', '9', '8', '5', '-', '-'],
        ['6', '5', '-', '3', '1', '-', '-', '-', '2'],
        ['5', '6', '3', '8', '-', '1', '4', '-', '9'],
        ['-', '9', '-', '-', '-', '-', '-', '-', '8'],
        ['1', '-', '8', '9', '-', '2', '3', '6', '5'],
        ['7', '-', '5', '-', '8', '3', '2', '9', '-'],
        ['8', '3', '-', '-', '2', '-', '-', '5', '-'],
        ['9', '-', '-', '4', '6', '-', '-', '3', '7']
    ]


def test_ligne():
    """
    Formule propositionnelle pour attribuer sur une ligne de 4 case
    l'attribution d'une valeur in range(1, 4), ou la valeur apparait uniquement une fois

    Exemple:
        [3, 2, 1, 4]

        avec {'x03: True, x12: True, x21: True, x34: True'}


    Fonction test pour l'implementation du formulateur propositionnelle de sudoku

    """
    length = 4

    clauses = []
    clause = []

    for i in range(0, length):
        clause.clear()

        for value in range(1, length + 1):
            string = 'x' + str(i) + str(value)
            clause.append(string)

        clauses.append(list(clause))

    clause.clear()

    for value in range(1, length + 1):
        for i in range(0, length):
            for k in range(i + 1, length):
                # xand
                clauses.append([f'not x{i}{value}', f'not x{k}{value}'])

    return clauses


def var(row, column, value):
    return f'x,{row},{column},{value}'


def unvar(var):
    """
    return list as [row, column, value]
    """
    return var.split(',')[1:]


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
    # Conjonctions de disjonctions
    clauses = []
    clause = []
    squared = n * n

    # Initialiser avec les nombres deja presents dans le sudoku
    for row in range(squared):
        for column in range(squared):
            if sudoku[row][column] != '-':
                clauses.extend([var(row, column, int(sudoku[row][column]))])

    # 1)
    for row in range(squared):
        for column in range(squared):
            clause.clear()
            for value in range(1, squared):
                clause.append(var(row, column, value))
            clauses.extend(clause)

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
            for value in range(1, squared):
                for pair in range(row, squared):
                    clauses.extend([
                        f'not {var(row, column, value)}',
                        f'not {var(row, pair, value)}'
                    ])

    # 3)
    # Meme proceder pour les colonnes que pour les lignes
    for column in range(squared):
        for row in range(squared):
            for value in range(1, squared):
                for pair in range(row, squared):
                    clauses.extend([
                        f'not {var(row, column, value)}',
                        f'not {var(pair, column, value)}'
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
    for row in range(0, squared, n):
        for column in range(0, squared, n):

            for value in range(1, squared):

                for i in range(n):
                    for j in range(n):

                        for i_pair in range(i, n):
                            for j_pair in range(j, n):
                                clauses.extend([
                                    f'not {var(row+i, column+j, value)}',
                                    f'not {var(row+i+i_pair, column+j+j_pair, value)}'
                                ])

    return clauses


if __name__ == '__main__':
    clauses = test_ligne()
    print(clauses)
    res = DPLL(clauses, CNF_variables(clauses))

    actual_res = {}
    for key, value in res.items():
        if value is True:
            actual_res[key] = value

    print(actual_res)
