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
  print (knoten.id) # testen
  #print (knoten.bucket[0]) # testen

  listen_socket = server("open");
  while True:
    connection, client_address = listen_socket.accept() # auf Verbindung warten
    #print ("got it") # testen (Verbindung aufgebaut)

    version = connection.recv(4).decode() # version of client
    todo = connection.recv(4).decode() # what the Client want to do
    print ("version: ",str(version)," todo: ",str(todo))

    ''' Client wants to search for ID '''
    if int(todo) is 1:
      data = connection.recv(20).decode() # erhalte 20 Bytes (20-stellige ID) und decode diese
      if 'close' in str(data):
        break
      print ("erhaltene Daten: ",(data)) # test (erhaltene ID ausgeben)
      knoten.bucket_add(int(data),"192.168.1.1","1234") # ID hinzufuegen
      print (knoten.bucket) # print complete bucket
    elif int(todo) is 0: # test cases
      data = connection.recv(20).decode() # erhalte 20 Bytes (20-stellige ID) und decode diese
      if 'close' in str(data):
        break
      print ("zu suchende ID: ",(data)) # test (erhaltene ID ausgeben)
      returns = knoten.find_id(int(data))
      connection.sendall(pickle.dumps(returns)) # serialize to send
      print (returns)
    else:
      print ("error beim finden in main")
    
  server("close",listen_socket);

main();
