from utils import validate_and_litterals
from tree import *


if __name__ == '__main__':
    prop = "x and not y"
    litts = validate_and_litterals(prop)

    prop2 = "x and ( not y or z )"
    litts2 = validate_and_litterals(prop2)

    print(recursive_tree(litts, prop))

    print(fifo(litts2, prop2))
    print(recursive_tree(litts2, prop2))
