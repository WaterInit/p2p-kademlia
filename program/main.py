import socket, pickle
import sys
from node import node

### all Hosts ###
#server_address = (socket.gethostname(), 0) # all other Hosts
bucket_size = 4 # size of bucket
    


def main():
  ### initialize Host ###
  knoten = node() # initialize node
  print(knoten.myid,knoten.listen_socket.getsockname()[0],knoten.listen_socket.getsockname()[1]) # testen
  #some other Host given # initialize to existing Network
  if len(sys.argv) > 1:
    knoten.bucket_add(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]))
    knoten.find_key(knoten.myid)
  ### initialize end ###

  ### tests ###
  #server("close",listen_socket);
  #return 0
  


  while True:
    print ("start")
    connection, client_address = knoten.listen_socket.accept() # wait for Connection
    #print ("got it") # testen (Verbindung aufgebaut)

    ### get version and todo ###
    infos = pickle.loads(connection.recv(1024))
    version = infos[0]
    todo = infos[1]
    #print ("version: ",str(version)," todo: ",str(todo)) # test
    connection.sendall(("0").encode()) # answer to distinguish bit-streams

    ### get contact-information ###
    c_infos = pickle.loads(connection.recv(1024)) # Client (id,ip,port)
    #print ("Client Infos: ",str(c_infos)) # test only
    connection.sendall(("0").encode()) # answer to distinguish bit-streams
    knoten.bucket_add(c_infos[0],c_infos[1],c_infos[2]) # ID hinzufuegen

    ### test case ###
    if int(todo) is 0:
      s_key = int(connection.recv(4).decode()) # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
      print ("erhaltene Daten: ",(s_key)) # test (erhaltene ID ausgeben)
      print (knoten.bucket) # print complete bucket

    ### Client wants to search for ID ###
    elif int(todo) is 1: # test cases
      s_key = int(connection.recv(4).decode()) # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
      #print ("zu suchende ID: ",(s_key)) # test (erhaltene ID ausgeben)
      returns = knoten.find_id(s_key)
      connection.sendall(pickle.dumps(returns)) # serialize to send
      #print (knoten.bucket)
      #print (returns)

    ### get unknown ID
    else: # TODO maybe do something
      print ("error beim finden in main")
    
  server("close",knoten.listen_socket);

main();
