import sys
from node import node


def main():
	# some other Host given # initialize to existing Network
	if len(sys.argv) > 1:
		knoten = node(sys.argv[1], int(sys.argv[2]))
	else:
		knoten = node(0, 0)
	# initialize end ###

	while True:
		user_todo = input("")


main()
