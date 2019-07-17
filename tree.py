from collections import deque
from CNF_utils import evaluate_assign_CNF
from copy import copy, deepcopy

"""
Trying to solve a SAT problem with a search tree

Les noeuds ou la racine represente une variable,
chaque noeuds possede deux fils pour leurs 2 interpretations
possible, True et False.

Une feuille dans l'arbre represente une interpretation de la
formule propositionnelle avec une assignation possible de chaque variables
de cette formule.

Le nombre d'assignations possibles = 2^n
ou n est le nombre de variable

1 is True
0 is False

Exemple:
 - 3 variables
racine |  noeuds    | feuilles
----------------------------
                        1

                1= x3

                        0
        1= x2

                        1

                0= x3

                        0
x1
                        1

                1= x3

                        0

        0= x2
                        1

                0= x3

                        0
On retrouve bien nos 8 possibilites.
"""


def recursive_tree(variable, formul):
    """
    On construit la racine

    Fournit toutes les assignations satisfiant la formule
    """

    interp = {variable[0]: False}

    # on commence par le cote gauche
    left_sol = build_and_search(variable[1:], interp, formul)

    # puis le cote droit
    interp[variable[0]] = True

    right_sol = build_and_search(variable[1:], interp, formul)

    return left_sol + right_sol


def build_and_search(variable, interp, formul):

    if len(variable) == 0:
        # on eval avec l'interpretation actuelle
        res = eval(formul, None, interp)

        if res:
            return [interp]
        else:
            return []

    interp[variable[0]] = False
    left_sol = build_and_search(variable[1:], interp, formul)

    interp[variable[0]] = True
    right_sol = build_and_search(variable[1:], interp, formul)

    return left_sol + right_sol


def fifo(variable, formul):
    """
    Fournit Une assignation valide pour la formule
    """
    deck = deque()

    index_by_name = dict(zip(variable, range(len(variable))))
    interp = dict(zip(variable, [None for i in variable]))
    size = len(variable)

    # False
    deck.append(variable[0])
    # True
    deck.append(variable[0])
    head = None

    while deck:

        head = deck.popleft()

        if interp[head] is None:
            interp[head] = False
        else:
            interp[head] = True

        for el in variable[index_by_name[head] + 1:]:
            # False
            deck.append(el)
            # True
            deck.append(el)

        if index_by_name[head] == size - 1:

            if eval(formul, None, interp):
                return interp

    return {}


def DPLL(CNF, variables, nb_iter):

    interp = {}
    last_epoque = None

    # tant que la taille de l'interpretation augmente on continue
    # s'arrete quand pts fixe trouve
    while last_epoque is None or len(interp) != last_epoque:

        # on force l'affectation des clauses unitaires
        for clause in CNF:
            for litteral in clause:
                if len(litteral) == 1:
                    if 'not' in litteral:
                        interp[litteral.replace('not', '').strip()] = False
                    else:
                        interp[litteral.strip()] = True

        CNF = evaluate_assign_CNF(CNF, interp)

        if CNF is False:
            return False
        elif CNF is True:
            return interp
        else:
            last_epoque = len(interp)
            
    print('---------------------------------------')
    print(nb_iter)
    print(CNF)

    left = evaluate_assign_CNF(deepcopy(CNF), {variables[0]: False})
    right = evaluate_assign_CNF(CNF, {variables[0]: True})

    if left is True:
        return {variables[0]: False}
    elif right is True:
        return {variables[0]: True}
    elif left is False and right is False:
        return False

    if left is not False:
        res = DPLL(left, variables[1:], nb_iter+1)

        if res is not False:
            return {**dict([(variables[0], False)]), **res}

    if right is not False:
        res = DPLL(right, variables[1:], nb_iter+1)

        if res is not False:
            return {**dict([(variables[0], True)]), **res}

    return False
