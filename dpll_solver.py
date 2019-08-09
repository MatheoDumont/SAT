from multiprocessing import Queue, Process
from copy import copy, deepcopy
from cnf_utils import *


def evaluate_dc(entry, interpretation):
    """
    Evalue une clause disjonctive avec une interpretation des variables contenues dans entry
    """
    if len(entry) == 0:
        return True

    for litt in entry:

        if litt < 0:
            litt = abs(litt)

            if litt in interpretation:
                if interpretation[litt] is False:
                    return True

        else:

            if litt in interpretation:
                if interpretation[litt] is True:
                    return True

    return False


def evaluate_assign_cnf(entry, interpretation):
    """

    Assigne une variable ou plusieurs variables contenues dans une list de clause.

    1)  Si une clause est valide, on la supprime de la list de clause.

    2)  Si elle n'est pas valide, cela signifie que les variables proposees 
        dans l'interpretation ne servent pas.
        On regarde donc chaque litteral de la clause pour le supprimer de la clause
        s'il est present dans l'interpretation.

    3)  Si une clause se retrouve vide par ce procede, alors l'interpretation 
        rend la formule UNSAT, et donc la fonction retourne False.

    4)  A la fin de l'execution, si la list de clause est vide, et donc que toutes
        les clauses ont ete valides, alors retourne True.

    En complexite, le pire cas est celui ou interpretation est vide.
    """

    if len(entry) == 0:
        return True

    if len(interpretation) == 0:
        return entry

    i = 0
    while i < len(entry):

        # 1)
        if evaluate_dc(entry[i], interpretation):
            del entry[i]

        else:

            j = 0
            while j < len(entry[i]):

                # 2)
                if abs(entry[i][j]) in interpretation:
                    del entry[i][j]
                else:
                    j += 1

                # 3)
                if len(entry[i]) == 0:
                    return False

            i += 1

    # 4)
    if len(entry) == 0:
        return True

    return entry


def unit_prop_and_pure_var(CNF, interp):
    # Pour les litteraux avec une seul polarite,
    # (ils apparaissent dans toute la cnf seulement True ou False)
    # On peut donc les affecter pour satisfaire des clauses

    false_lit = set()
    true_lit = set()

    # tant que la taille de l'interpretation augmente on continue
    # s'arrete quand pts fixe trouve
    epoque = len(interp)
    last_epoque = None

    while last_epoque is None or epoque != last_epoque:

        # on force l'affectation des clauses unitaires
        for clause in CNF:

            # Variable pure
            for lit in clause:
                if lit > 0 and lit not in true_lit:
                    true_lit.add(lit)
                elif lit not in false_lit:
                    false_lit.add(abs(lit))

            if len(clause) == 1:
                to_be_interpreted_as = None
                lit = abs(clause[0])

                if clause[0] < 0:
                    to_be_interpreted_as = False
                else:
                    to_be_interpreted_as = True

                if lit in interp:
                    if interp[lit] is not to_be_interpreted_as:
                        return False
                else:
                    interp[lit] = to_be_interpreted_as

        # Variable pure
        for el in true_lit - false_lit:
            if el in interp:
                if not interp[el]:
                    return False
            else:
                interp[el] = True

        for el in false_lit - true_lit:
            if el in interp:
                if interp[el]:
                    return False
            else:
                interp[el] = False

        CNF = evaluate_assign_cnf(CNF, interp)

        if CNF is False:
            return False
        elif CNF is True:
            return interp,
        else:
            last_epoque = epoque
            epoque = len(interp)

    return interp, CNF


def choose_var(cnf):

    try:
        return cnf[0][0]
    except Exception as e:
        raise e("choose_var essaye de retourner cnf[0][0]")


def init_var_clauses(cnf):

    var_link_clause = dict()

    for i in range(len(cnf)):
        for j in range(len(cnf[i])):
            if not var_link_clause[abs(clauses[i][j])] in var_link_clause:
                var_link_clause[abs(clauses[i][j])] = []
            var_link_clause[abs(clauses[i][j])].append((i, j))

    return var_link_clause


def DPLL(CNF, interp=None):
    """
    Algorithme DPLL

    CNF: from cnt_utils.cnf_clauses()
    """

    results = unit_prop_and_pure_var(CNF, {} if interp is None else interp)

    if type(results) is tuple:
        if len(results) == 1:
            return interp
        else:
            interp, CNF = results
    else:
        return False

    var = choose_var(CNF)

    sat = DPLL(deepcopy(CNF), {var: False}) or DPLL(CNF, {var: True})

    if sat is False:
        return False

    return {**interp, **sat}


def multiproc_DPLL(cnf):

    # -unit prop
    # -variable pure
    # -Queue de process
    # dans laquelle on met les recherches de droite et gauche
    # garder la trace des interpretation dans un dict
    # et faire la back prop dans la cas ou la branche est False
    # Exemple: genre, donner un numero unique a une interp de branche
    # et pouvoir pour une branche UNSAT, back-propager dans le dict d'interp
    # pour supprimer les interps des branches resultant UNSAT

    q = Queue()
