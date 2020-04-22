_keywords = ['and', 'or', 'not', '(', ')']

"""
Pour ecrire une formule, utilisez la forme seulement les keywords 
mentionnes au-dessus 

Exemple: "x and not (y or z)"

DEPRECATED: Not updated since
"""


def variables(prop):
    """
    Retourne seulement les variables sans tester la validiter
    de la prop. 

    prop: str
    """
    for key in _keywords:
        prop = prop.replace(key, '')

    variabs = set()

    for var in prop.split(' '):
        if var == '' or var == ' ':
            continue
        var = var.strip()
        if var not in variabs:
            variabs.add(var)

    return list(variabs)


def validate(prop):
    """
    Verifie la proposition de telle sorte que ce soit une formule
    booleenne valide.

    Renvoie les litteraux correspondant a la formule valide.

    L'eval raise une erreur s'il echoue.

    prop: str
    """
    if prop is None:
        return

    variabs = variables(prop)

    dict_lit = {}

    for l in variabs:
        dict_lit[l] = False

    # we test it
    eval(prop, dict_lit)

    # we past the test
    # the litterals
    return variabs


def evaluate(clause, interpretation, variabs=None):
    """
    Utile pour evaluer une formule sans assigner toutes les variables.

    Interpretation peut contenir des variables qui n'ont pas rapport
    avec la clause, rien n'en sera fait cependant.

    On peut ne pas tenir cas de la taille d'interpretation etant
    donne que c'est un dict avec O(1) en acces.

    clause: str
    interpretation: dict
    """

    variabs = variables(clause) if variabs is None else variabs

    for var in variabs:
        if var not in interpretation:
            interpretation[var] = False

    return eval(clause, None, interpretation)


if __name__ == '__main__':
    prop = "x and not (y or z)"

    print(prop)

    print(evaluate(prop, {'x': True}))

    print(evaluate('(x or y or z)', {'z': False}))
