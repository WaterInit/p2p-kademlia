import socket, pickle
import sys
from node import node

### all Hosts ###
server_address = (socket.gethostname(), 0) # all other Hosts
my_version = "0001" # first Version

# Server definieren, socket oeffnen
def server(*todo): # first arg = what to do, second arg = optional socket-object
  if todo[0] is 'open':
    #print ("laeuft") # testen (server gestartet)
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
    listen_socket.bind(server_address) # socket an IP und Port binden
    listen_socket.listen(5) # socket als listen definieren
    #print (listen_socket.getsockname())
    return listen_socket

  elif todo[0] is 'close':
    todo[1].close()
    print ("socket schliessen")

  else:
    print ("nichts")

# finde eine ID im Netzwerk
#def find_id(s_id):


def init_node(knoten): # initialize node in network
  #known_host = (127.0.0.1)
  #bucket_add(
  find_id(knoten.myid); # give back a bucket


def main():
  ### initialize Host ###
  #some other Host given
  if len(sys.argv) > 1:
    #print (sys.argv[1],sys.argv[2],sys.argv[3])
    while True:
      knoten = node() # initialize node
      knoten.bucket_add(int(sys.argv[1]),sys.argv[2],int(sys.argv[3])) # add known host to bucket
      if init_node(knoten) is 0: # initialize to existing Network
        break
  else: # thats the first node
    knoten = node()
  #print (knoten.bucket) # testen
  listen_socket = server("open");
  print(knoten.myid,listen_socket.getsockname()[0],listen_socket.getsockname()[1])


  server("close",listen_socket);
  return 0
  
  ### initialize end ###


  while True:
    connection, client_address = listen_socket.accept() # auf Verbindung warten
    #print ("got it") # testen (Verbindung aufgebaut)

    version = connection.recv(4).decode() # version of client
    connection.sendall(("0").encode()) # Antwort senden um bit-stroeme zu unterscheiden
    if int(version) is 0: # stop Server for test cases
      break

    todo = connection.recv(4).decode() # what the Client want to do
    connection.sendall(("0").encode()) # Antwort senden um bit-stream zu unterscheiden
    print ("version: ",str(version)," todo: ",str(todo))
    c_id = int(connection.recv(4).decode()) # Client id
    connection.sendall(("0").encode()) # Antwort senden um bit-stroeme zu unterscheiden
    knoten.bucket_add(c_id,client_address[0],client_address[1]) # ID hinzufuegen

    ### test case ###
    if int(todo) is 0:
      s_key = int(connection.recv(4).decode()) # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
      print ("erhaltene Daten: ",(s_key)) # test (erhaltene ID ausgeben)
      print (knoten.bucket) # print complete bucket

    ### Client wants to search for ID ###
    elif int(todo) is 1: # test cases
      s_key = int(connection.recv(4).decode()) # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
      print ("zu suchende ID: ",(s_key)) # test (erhaltene ID ausgeben)
      returns = knoten.find_id(s_key)
      connection.sendall(pickle.dumps(returns)) # serialize to send
      print (knoten.bucket)
      #print (returns)

    ### get unknown ID
    else: # TODO maybe do something
      print ("error beim finden in main")
    
  server("close",listen_socket);

main();
