import sys
from node import node


def main():
	# some other Host given # initialize to existing Network
	if len(sys.argv) > 1:
		knoten = node(sys.argv[1], int(sys.argv[2]))
	else:
		knoten = node(0, 0)
	# print own socket-information
	print(knoten.myid, knoten.listen_socket.getsockname()[0], knoten.listen_socket.getsockname()[1])
	# initialize end ###

	while True:
		user_todo = input("")
		ret = knoten.action(user_todo)
		if ret == 1:  # beenden
			break


main()
