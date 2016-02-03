import socket, pickle
import sys
from node import node
    
def main():
  ### initialize Host ###
  knoten = node() # initialize node
  # print own socket-information
  print(knoten.myid,knoten.listen_socket.getsockname()[0],knoten.listen_socket.getsockname()[1])
  #some other Host given # initialize to existing Network
  if len(sys.argv) > 1:
    # add known host to own bucket
    knoten.bucket_add(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]))
    # search own id in network
    knoten.find_key(knoten.myid)
  ### initialize end ###

  while True:
    input("")
  server("close",knoten.listen_socket);

main();
