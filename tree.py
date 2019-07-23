from collections import deque
from cnf_utils import evaluate_assign_CNF
from copy import copy, deepcopy

"""
Trying to solve a SAT problem with a search tree

Les noeuds ou la racine represente une variable,
chaque noeuds possede deux fils pour leurs 2 interpretations
possible, True et False.

Une feuille dans l'arbre represente une interpretation de la
formule propositionnelle avec une assignation possible de chaque `
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


def DPLL(CNF, set_variables):
    """
    Algorithme DPLL

    CNF: from CNF_clauses()
    set_variables: set of variables from CNF_variables(CNF, to_list=False)
    """

    def nested(CNF, set_variables, interp):

        if interp:
            CNF = evaluate_assign_CNF(CNF, interp)

            if CNF is True:
                return interp
            elif CNF is False:
                return False

        # Si la, donc CNF utilisable
        last_epoque = None

        # tant que la taille de l'interpretation augmente on continue
        # s'arrete quand pts fixe trouve
        while last_epoque is None or len(interp) != last_epoque:

            # on force l'affectation des clauses unitaires
            for clause in CNF:
                if len(clause) == 1:
                    to_be_interpreted = None
                    lit = abs(clause[0])

                    if clause[0] < 0:
                        to_be_interpreted = False
                    else:
                        to_be_interpreted = True

                    if lit in interp:
                        if interp[lit] is not to_be_interpreted:
                            return False
                    else:
                        interp[lit] = to_be_interpreted

            CNF = evaluate_assign_CNF(CNF, interp)

            if CNF is False:
                return False
            elif CNF is True:
                return interp
            else:
                last_epoque = len(interp)

        # On met a jour les variables
        # par rapport a l'interpretation faite
        set_variables = set_variables.difference(set(interp.keys()))
        var = set_variables.pop()

        left = nested(deepcopy(CNF), set_variables, {var: False})

        # si left est valide
        if left is not False:
            return {**interp, **left}

        # sinon on test le cote droit
        right = nested(CNF, set_variables, {var: True})

        # si right est valide
        if right is not False:
            return {**interp, **right}

        # la formule ne peut pas etre validee avec l'interpretation actuelle
        return False

    return nested(CNF, set_variables, {})
