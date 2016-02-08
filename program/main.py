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
		if user_todo == "put":
			key = input("")
			knoten.insert_key(key, key)
		elif user_todo == "get":
			key = input("")
			ret = knoten.get_key(key)
			print(ret)
		else:
			print (user_todo)


main()
