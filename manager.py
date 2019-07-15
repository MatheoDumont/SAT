_keywords = ['and', 'or', 'not', '(', ')']

"""
DISCLAIMER : the manager use eval(),
don't run in some stupid things

To write formula use the keywords mentioned above
like this : "x and not y" or "x and (not x and y)"
"""


class Manager:

    def __init__(self, prop=None):
        """
        prop is suppose to be a string
        """
        self._handle_prop(prop)

    def _handle_prop(self, prop):

        if prop is None:
            self.litterals = []
            self.prop = ''
            return

        splitted = prop.split(' ')

        litterals = []
        for elem in splitted:
            if elem not in _keywords:
                if elem not in litterals:
                    litterals.append(elem)

        dict_lit = {}

        for l in litterals:
            dict_lit[l] = False

        # we test it
        eval(prop, dict_lit)

        # we past the test
        self.litterals = litterals
        self.prop = prop



