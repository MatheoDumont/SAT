"""
Archivage de DPLL_solver avec les variables linke entres elles
pour suppposement modifier les clauses existantes a l'aide des indices
des vars, mais trop dure a mettre en place, plus tard peut etre.
"""

from dpll_solver import *


def evaluate_assign_cnf_linked(clauses, interpretation, linked):
    """
    clauses: list de list sous forme cnf
    linked: dict de dict
    interpretation: dict
    """

    if len(clauses) == 0:
        return True

    if len(interpretation) == 0:
        return entry

    for current_var, current_var_eval in interpretation.items():
        if current_var in linked:

            for clause, pos_in_clause in linked[current_var].items():

                to_del_clause = False
                # Si litteral pas faux, donc > 0
                if clauses[clause][pos_in_clause] > 0:
                    if current_var_eval is True:

                        for litteral in clauses[clause]:

                            if abs(litteral) != current_var:
                                del linked[abs(litteral)][clause]

                        to_del_clause = True
                    else:
                        del clauses[clause][pos_in_clause]

                elif clauses[clause][pos_in_clause] < 0:
                    if current_var_eval is False:

                        for litteral in clauses[clause]:

                            if abs(litteral) != current_var:
                                del linked[abs(litteral)][clause]

                        to_del_clause = True
                    else:

                        del clauses[clause][pos_in_clause]

                if len(clauses[clause]) == 0:
                    return False
                elif to_del_clause:
                    del clauses[clause]

            del linked[current_var]

    if len(clauses) == 0:
        return True

    return clauses, linked


def unit_prop_and_pure_var(CNF, interp, linked):
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

        results = evaluate_assign_cnf_linked(CNF, interp, linked)

        if type(results) is tuple:
            CNF, linked = results
        elif results is False:
            return False
        elif results is True:
            return interp,
        else:
            last_epoque = epoque
            epoque = len(interp)

    return interp, CNF, linked


def build_link(cnf):
    """
    Lien, pour chaque variable, on sauvegarde l'indice des clauses dans 
    lesquelles ces variables apparaissent, ainsi que leurs position
    dans ces clauses.

    linked = {
        # la variable 1
        1: {
            # dans la clause 1456 a la position 3
            1456: 3
        }
        ...
    }
    """
    linked = dict()

    for i in range(len(cnf)):
        for j in range(len(cnf[i])):
            if not abs(cnf[i][j]) in linked:

                linked[abs(cnf[i][j])] = dict()

            linked[abs(cnf[i][j])][i] = j

    return linked


def DPLL(CNF, interp=None, linked=None):
    """
    Algorithme DPLL

    """

    results = unit_prop_and_pure_var(
        CNF,
        {} if interp is None else interp,
        build_link(CNF) if linked is None else linked
    )

    if type(results) is tuple:
        if len(results) == 1:
            return interp
        else:
            interp, CNF, linked = results
    else:
        return False

    var = choose_var(CNF)

    sat = DPLL(deepcopy(CNF), {var: False}, deepcopy(linked)
               ) or DPLL(CNF, {var: True}, linked)

    if sat is False:
        return False

    return {**interp, **sat}
