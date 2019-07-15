from collections import deque

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
