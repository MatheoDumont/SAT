from copy import copy, deepcopy
"""
Ce module pourvoie des fonctions utilitaires a appliquer
sur des formules en CNF

Qui sont des conjonctions de disjonctions 

CLAUSE DISJONCTIVE de la forme:
"(x or y or not x or ...)"

Et conjonction de la forme:
"(x and y and not x and ...)"

(avec ou sans les parentheses)

La fonction principale ici est CNF_clauses, elle tranforme une str
sous forme CNF en list de list de variables.

Exemple:
str_cnf = "(x or y) and ( not z or w)"
result = CNF_clauses(str_cnf)
print(result) # [['x', 'y'], ['not z', 'w']]

"""


def transform_pycosat(clauses):
    for i in range(len(clauses)):
        for j in range(len(clauses[i])):
            clauses[i][j] = clauses[i][j].replace('not', '-').replace(' ', '')

    for i in range(len(clauses)):
        for j in range(len(clauses[i])):
            clauses[i][j] = int(clauses[i][j])

    return clauses


def is_cnf(func):

    def inner(*args, **kwargs):
        error_msg_list = "'args[0]' should be 'list' of 'list'"
        error_msg_elmt = "Elements of a 'clause' should only be 'str'"

        if type(args[0]) is not list:
            raise TypeError(f'{error_msg_list},  args[0]:{args[0]}')

        for supposed_clause in args[0]:
            if type(supposed_clause) is not list:
                raise TypeError(f'{error_msg_list},  "{supposed_clause}"')
            for el in supposed_clause:
                if type(el) is not str:
                    raise TypeError(f'{error_msg_elmt},  "{el}"')

        return func(*args, **kwargs)

    return inner


def CNF_clauses(prop):
    """
    Utilitaire pour obtenir les clauses d'une formule sous forme 
    CNF ou Formule Normale Conjonctive donc de la forme:

    "(a or b or ...) and (c or not d or ...) ... "

    Retourne un resultat sous la forme:
    0: ['a','b']
    1: ['c', 'not d']
    .
    .
    .
    n: ...

    chaque clauses[i][j] est evaluable
    tel que eval(clauses[i][j], None, {var: True})
    ou var est le nom de la variable contenu en a 
    clauses[i][j]

    """
    splitted = prop.split('and')
    clauses = []

    for clause in splitted:
        clause = clause.replace('(', '').replace(')', '')
        clauses.append(clause.split('or'))

    return clauses


@is_cnf
def CNF_variables(CNF, to_list=True):
    """
    'entry' doit etre issue de CNF_clauses()
    """
    variabs = set()

    for clause in CNF:
        for var in clause:
            var = var.replace('not', '').strip()
            if var not in variabs:
                variabs.add(var)

    if to_list is True:
        return variabs

    return list(variabs)


def evaluate_DC(entry, interpretation):
    """
    Evalue une clause disjonctive avec une interpretation des variables contenues dans entry
    """

    for litt in entry:

        if 'not' in litt:
            litt = litt.replace('not', '').strip()

            if litt in interpretation:
                if interpretation[litt] is False:
                    return True

        else:
            litt = litt.strip()

            if litt in interpretation:
                if interpretation[litt] is True:
                    return True

    return False


def evaluate_assign_CNF(entry, interpretation):
    """

    Assigne une variable ou plusieurs variables contenues dans une list de clause.

    Si une clause est valide, on la supprime de la list de clause.
    Si elle n'est pas valide, cela signifie que les variables proposees 
    dans l'interpretation ne servent pas.
    On regarde donc chaque litteral de la clause pour le supprimer de la clause
    s'il est present dans l'interpretation.

    Si une clause se retrouve vide par ce procede, alors l'interpretation 
    rend la formule UNSAT, et donc la fonction retourne False.

    A la fin de l'execution, si la list de clause est vide, et donc que toutes
    les clauses ont ete valides, alors retourne True.

    En complexite, le pire cas est celui ou interpretation est vide.
    """

    if len(entry) == 0:
        return True

    # Au cas ou, on retourne entry et non False car on ne sait pas
    # vu qu'il n'y pas de variables
    if len(interpretation) == 0:
        return entry

    i = 0
    while i < len(entry):

        if evaluate_DC(entry[i], interpretation):
            del entry[i]

        else:

            j = 0
            while j < len(entry[i]):
                if entry[i][j].replace('not', '').strip() in interpretation:
                    del entry[i][j]
                else:
                    j += 1

                if len(entry[i]) == 0:
                    return False

            i += 1

    if len(entry) == 0:
        return True

    return entry


# if __name__ == '__main__':
#     cnf = "(x or y) and (not x or z)"
#     print(cnf)

#     print("-------------------CNF_clauses------------------")
#     clauses = CNF_clauses(cnf)
#     print(clauses)

#     print("-------------------variables--------------------")
#     print(variables_CNF(clauses))
#     print(variables_CNF(clauses[0]))

#     print("-------------------evaluate---------------------")
#     print(evaluate_DC(clauses[0], {'x': True}))  # True
#     print(evaluate_DC(clauses[1], {'x': True}))  # False

#     """
#     3 cas a verifier pour evaluate_assign:

#     Pour une list de clause
#         1) retourne True donc valide entry avec interp donne
#         2) retourne False donc invalide entry avec interp donne
#         3) rend list de clause invalide et assigne(donc avec des clauses ou litteraux supprimes)
#     """

#     print("------------------evaluate_assign---------------")
#     # 1)
#     print(evaluate_assign_CNF(deepcopy(clauses), {'x': True, 'z': True}))

#     # 2)
#     print(evaluate_assign_CNF(deepcopy(clauses), {'x': True, 'z': False}))

#     # 3)
#     print(evaluate_assign_CNF(deepcopy(clauses), {'x': True}))
