import socket, pickle
import sys
from node import node
import random

server_address = (socket.gethostname(), 1246)


# Client definieren
def client(todo):
  bucket_size = 4

  version = "0001"
  todo = "0001"

  #message = '11001001100010011011' # simbolisiert die ID
  myid = format(random.getrandbits(bucket_size))
  #myid = sys.argv[1]
  s_key = format(random.getrandbits(bucket_size))
  if 'quit' in sys.argv[1]:
    version = "0000"


  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
  client_socket.connect(server_address) # Verbindung zum Server aufbauen

  client_socket.sendall(version.encode()) # version 0001 und 0000=keyuebergeben (testen)
  if int(client_socket.recv(4).decode()) is not 0: # Antwort senden um bit-stroeme zu unterscheiden
    print("Fehler")
    return 0
  client_socket.sendall(todo.encode()) # todo 0001=testen
  if int(client_socket.recv(4).decode()) is not 0: # Antwort senden um bit-stroeme zu unterscheiden
    print("Fehler")
    return 0
  client_socket.sendall(myid.encode()) # ID senden und encoden (in bytes casten)
  if int(client_socket.recv(4).decode()) is not 0: # Antwort senden um bit-stroeme zu unterscheiden
    print("Fehler")
    return 0
  client_socket.sendall(s_key.encode())
  print ("ID: ",str(myid)," key: ",str(s_key))

  if int(todo) is 1:
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
