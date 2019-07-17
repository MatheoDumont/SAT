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


def is_list_of_clause(entry):
    is_listoflist = False
    # si une list de clause
    try:
        is_listoflist = type(entry[0]) is list

    except Exception as e:
        # rien a faire
        pass

    return is_listoflist


def variables_CNF(entry):
    """
    'entry' peut etre soit une clause 
    soit une list de clause 
    """
    variabs = set()

    if is_list_of_clause(entry):
        for clause in entry:
            for var in clause:
                var = var.replace('not', '').strip()
                if var not in variabs:
                    variabs.add(var)

    else:
        for var in entry:
            var = var.replace('not', '').strip()
            if var not in variabs:
                variabs.add(var)

    return variabs


def evaluate_CNF(entry, interpretation):
    """
    Evalue une clause avec une interpretation des variables contenues dans entry
    """

    evaluation = 'False'
    for litt in entry:
        if litt.replace('not', '').strip() in interpretation:
            evaluation = evaluation + ' or ' + litt

    return eval(evaluation, None, interpretation)


def evaluate_assign(entry, interpretation):
    """

    Assigne une variable ou plusieurs variables contenues dans une list de 
    variable ou dans une list de clause.

    Pour une clause, si les assignations la rende SAT, renvoie True
    sinon renvoie la clause sans la variable consideree comme 
    fausse: clause - interpretation

    Pour une list de clause, renvoie cette list en assignant la ou les variable(s)
    avec leurs interpretations dans les clauses ou elles apparaissent.
    Si cela valide l'une des clauses, alors celle-ci est supprimee de la list.
    Si toutes les clauses sont supprimes ainsi alors renvoie True(SAT).

    Dans le cas une interpretation rend une clause fausse
    et que toutes les variables de cette clause sont presente dans
    l'interpretation, retourne False.

    Exemple:

        interp = {'x': True, 'y': False}
        entry = "not x or y"

        return False if not evaluate(entry, interp) and variables(entry) == interp

    """

    if len(entry) == 0:
        return True

    if is_list_of_clause(entry):

        i = 0
        while i < len(entry):

            if evaluate_CNF(entry[i], interpretation):
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

    else:

        if evaluate_CNF(entry, interpretation):
            return True
        else:
            i = 0
            while i < len(entry):
                if entry[i].replace('not', '').strip() in interpretation:
                    del entry[i]
                else:
                    i += 1

                if len(entry) == 0:
                    return False
    return entry


if __name__ == '__main__':
    cnf = "(x or y) and (not x or z)"
    print(cnf)

    print("-------------------CNF_clauses------------------")
    clauses = CNF_clauses(cnf)
    print(clauses)

    print("-------------------variables--------------------")
    print(variables_CNF(clauses))
    print(variables_CNF(clauses[0]))

    print("-------------------evaluate---------------------")
    print(evaluate_CNF(clauses[0], {'x': True}))  # True
    print(evaluate_CNF(clauses[1], {'x': True}))  # False

    """
    4 cas a verifier pour evaluate_assign:
    
    Pour une list de clause
        1) retourne True donc valide entry avec interp donne
        2) retourne False donc invalide entry avec interp donne
        3) rend list de clause invalide et assigne(donc avec des clauses ou litteraux supprimes)

    Pour une clause
        4) retourne True donc valide entry avec interp donne
        5) retourne False donc invalide entry avec interp donne
        6) retourne la clause invalide et assigne(donc avec des litteraux supprimes)
    """

    print("------------------evaluate_assign---------------")
    # 1)
    print(evaluate_assign(deepcopy(clauses), {'x': True, 'z': True}))

    # 2)
    print(evaluate_assign(deepcopy(clauses), {'x': True, 'z': False}))

    # 3)
    print(evaluate_assign(deepcopy(clauses), {'x': True}))

    # 4)
    print(evaluate_assign(copy(clauses[0]), {'x': True}))

    # 5)
    print(evaluate_assign(copy(clauses[0]), {'x': False, 'y': False}))

    # 6)
    print(evaluate_assign(copy(clauses), {'x': False}))

