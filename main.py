from util import *
from tree import *


if __name__ == '__main__':
    prop = "x and not y"
    man = Manager(prop)

    prop2 = "x and ( not y or z )"
    man2 = Manager(prop2)

    print(recursive_tree(man.litterals, prop))

    print(fifo(man2.litterals, prop2))
    print(recursive_tree(man2.litterals, prop2))
