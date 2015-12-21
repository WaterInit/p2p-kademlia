import socket
import sys
from node import node

server_address = (socket.gethostname(), 1240)

# Server definieren
def server(todo):
  knoten = node() # initialize node
  print (knoten.id) # testen
  #print (knoten.bucket[0]) # testen
  if todo is 'open':
    print ("laeuft") # testen (server gestartet)
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
    listen_socket.bind(server_address) # socket an IP und Port binden
    listen_socket.listen(5) # socket als listen definieren
    return listen_socket

  ##### sinnloser Stuss Anfang #####
  elif todo is 'close':
    print ("stop it")
  else:
    print ("nichts")
  ##### sinnloser Stuss Ende #####


def main():
  listen_socket = server("open");
  while True:
    connection, client_address = listen_socket.accept() # auf Verbindung warten
    print ("got it") # testen (Verbindung aufgebaut)
    data = connection.recv(20).decode() # erhalte 20 Bytes (20-stellige ID) und decode diese
    print ("erhaltene Daten: ",repr(data)) # test (erhaltene ID ausgeben)


main();
