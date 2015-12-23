import socket, pickle
import sys
from node import node
import random

server_address = (socket.gethostname(), 1246)


# Client definieren
def client(todo):
  if todo is 'connect':
    #message = '11001001100010011011' # simbolisiert die ID
    message = format(random.getrandbits(20))
  elif todo is 'quit':
    message = 'close'
  else:
    print ("Fehler")
    return 0

  version = ("0001")
  todo = ("0000")

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
  client_socket.connect(server_address) # Verbindung zum Server aufbauen

  client_socket.sendall(version.encode()) # version 0001 und 0000=keyuebergeben (testen)
  client_socket.sendall(todo.encode()) # todo 0001=testen
  client_socket.sendall(message.encode()) # ID senden und encoden (in bytes casten)

  if int(todo) is 0:
    data = pickle.loads(client_socket.recv(1024))
    print (data)


  print ("Client is done") # test (fertig)


### ###
### entweder den Client oder den Server starten ###
### python3 main.py server
### python3 main.py client
### ###

print (sys.argv[1])
if 'quit' in sys.argv[1]:
  client("quit");
else:
  client("connect");
