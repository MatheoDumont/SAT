from manager import Manager
from tree import *


if __name__ == '__main__':
	prop = "x and not y"
	man = Manager(prop)

	prop2 = "x and ( not x or y )"
	man2 = Manager(prop2)

	print(man2.litterals)

	print(recursive_tree(man.litterals, prop))
	print(fifo(man.litterals, prop))

	print(fifo(man2.litterals, prop2))
