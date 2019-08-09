from copy import copy, deepcopy

import math
"""
Ce module pourvoie des fonctions utilitaires a appliquer
sur des formules en CNF(Conjonctive normal form)

Qui sont des conjonctions de disjonctions 

Clause disjonctive de la forme:
"(x or y or not x or ...)"

Clause Conjonctive de la forme:
"(x and y and not x and ...)"



(avec ou sans les parentheses)

'cnf_from_string', elle tranforme une str
sous forme CNF en list de list de variables.

Les variables doivent etres des entiers.

Les litteraux de ces variables sont positifs, 
ou negatifs pour representer des litteraux faux 
ou vrais.

Exemple:
str_cnf = "(1 or 2) and ( -3 or 4)"
result = cnf_from_str(str_cnf)
print(result) # [[1, 2], [-3, 4]]

"""


def is_cnf(func):

    def inner(*args, **kwargs):
        error_msg_list = "'args[0]' should be 'list' of 'list'"
        error_msg_elmt = "Elements of a 'clause' should only be 'integer'"

        if type(args[0]) is not list:
            raise TypeError(f'{error_msg_list},  args[0]:{args[0]}')

        for supposed_clause in args[0]:
            if type(supposed_clause) is not list:
                raise TypeError(f'{error_msg_list},  "{supposed_clause}"')
            for el in supposed_clause:
                if type(el) is not int:
                    raise TypeError(f'{error_msg_elmt},  "{el}"')

        return func(*args, **kwargs)

    return inner


def litteral(var, false=False):
    if false:
        return -var

    return var


def cnf_from_str(prop):
    """
    Utilitaire pour obtenir les clauses d'une formule sous forme 
    CNF ou Formule Normale Conjonctive donc de la forme:

    "(1 or 2 or ...) and (3 or  -2 or ...) ... "

    Retourne un resultat sous la forme:
    0: [1, 2]
    1: [3, -2]
    .
    .
    .
    n: ...

    Return: [[var1, var2], [var3, -var4], ...]

    """
    splitted = prop.split('and')
    clauses = []

    for clause in splitted:
        clause = clause.replace('(', '').replace(')', '')
        str_clause = clause.split('or')

        int_litterals = [int(el) for el in str_clause]

        clauses.append(int_litterals)
        
    return clauses


@is_cnf
def cnf_variables(cnf):
    """
    'entry' doit etre issue de cnf_clauses()

    return: 'set' de variable
    """
    variabs = set()

    for clause in cnf:
        for var in clause:
            var = abs(var)

            if var not in variabs:
                variabs.add(var)

    return variabs


