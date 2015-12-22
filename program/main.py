import socket
import sys
from node import node

server_address = (socket.gethostname(), 1240) # use specified Port to test
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
    print ("got it") # testen (Verbindung aufgebaut)
    data = connection.recv(20).decode() # erhalte 20 Bytes (20-stellige ID) und decode diese
    print ("erhaltene Daten: ",repr(data)) # test (erhaltene ID ausgeben)
    if 'close' in str(data):
      break
  server("close",listen_socket);

main();
