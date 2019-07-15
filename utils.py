_keywords = ['and', 'or', 'not', '(', ')']

"""
Pour ecrire une formule, utilisez la forme seulement les keywords 
mentionnes au-dessus 

Exemple: "x and not (y or z)"

CLAUSE DISJONCTIVE de la forme:
"(x or y or not x or ...)"

(avec ou sans les parentheses)
"""


def litterals(prop):
    """
    Retourne seulement les litteraux sans tester la validiter
    de la prop. 

    prop: str
    """
    for key in _keywords:
        prop = prop.replace(key, '')

    return list(prop.replace(' ', ''))


def validate_and_litterals(prop):
    """
    Verifie la proposition de telle sorte que ce soit une formule
    booleenne valide.

    Renvoie les litteraux correspondant a la formule valide.

    L'eval raise une erreur s'il echoue.

    prop: str
    """
    if prop is None:
        return

    litts = litterals(prop)

    dict_lit = {}

    for l in litts:
        dict_lit[l] = False

    # we test it
    eval(prop, dict_lit)

    # we past the test
    # the litterals
    return litts


def evaluate(clause, interpretation):
    """
    Utile pour evaluer une formule sans assigner toutes les variables.

    Interpretation peut contenir des variables qui n'ont pas rapport
    avec la clause, rien n'en sera fait cependant.

    On peut ne pas tenir cas de la taille d'interpretation etant
    donne que c'est un dict avec O(1) en acces.

    clause: str
    interpretation: dict
    """

    litts = litterals(clause)

    for litt in litts:
        if litt not in interpretation:
            interpretation[litt] = False

    return eval(clause, None, interpretation)


def CNF_clauses(prop):
    """
    Utilitaire pour obtenir les clauses d'une formule sous forme 
    CNF ou Formule Normale Conjonctive donc de la forme:

    "(a or b or ...) and (c or d or ...) ... "
    """
    return prop.split('and')


if __name__ == '__main__':
    prop = "x and not (y or z)"
    print(prop)
    print(litterals(prop))
    print(validate_and_litterals(prop))

    print(evaluate(prop, {'x': True}))

    print(evaluate('(x or y or z)', {'z': False}))

    print(CNF_clauses("(a or b or c ) and (sdfsdfs)"))
