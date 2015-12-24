import socket, pickle
import sys
from node import node

server_address = (socket.gethostname(), 1246) # use specified Port to test
#server_address = (socket.gethostname(), 0) # use random Port

# Server definieren, socket oeffnen
def server(*todo): # first arg = what to do, second arg = optional socket-object
  if todo[0] is 'open':
    print ("laeuft") # testen (server gestartet)
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
    listen_socket.bind(server_address) # socket an IP und Port binden
    listen_socket.listen(5) # socket als listen definieren
    print (listen_socket.getsockname())
    return listen_socket

  elif todo[0] is 'close':
    todo[1].close()
    print ("socket schliessen")

  else:
    print ("nichts")

# finde eine ID im Netzwerk
#def find_id(s_id):
  


def main():
  knoten = node() # initialize node
  print (knoten.myid) # testen
  #print (knoten.bucket[0]) # testen

  listen_socket = server("open");
  while True:
    connection, client_address = listen_socket.accept() # auf Verbindung warten
    #print ("got it") # testen (Verbindung aufgebaut)

    version = connection.recv(4).decode() # version of client
    connection.sendall(("0").encode()) # Antwort senden um bit-stroeme zu unterscheiden
    if int(version) is 0: # stop Server for test cases
      break

    todo = connection.recv(4).decode() # what the Client want to do
    connection.sendall(("0").encode()) # Antwort senden um bit-stroeme zu unterscheiden
    print ("version: ",str(version)," todo: ",str(todo))
    c_id = int(connection.recv(4).decode()) # Client id
    connection.sendall(("0").encode()) # Antwort senden um bit-stroeme zu unterscheiden
    print("client ID: ",str(c_id))
    knoten.bucket_add(c_id,"192.168.1.1","1234") # ID hinzufuegen

    ### test case ###
    if int(todo) is 0:
      print ("test")
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
      print (returns)
    else:
      print ("error beim finden in main")
    
  server("close",listen_socket);

main();
