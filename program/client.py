import socket
import sys
from node import node

server_address = (socket.gethostname(), 1240)


# Client definieren
def client(todo):
  if todo is 'connect':
    message = '11001001100010011011' # simbolisiert die ID
  elif todo is 'quit':
    message = 'close'
  else:
    print ("Fehler")
    return 0

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
  client_socket.connect(server_address) # Verbindung zum Server aufbauen

  client_socket.sendall(message.encode()) # ID senden und encoden (in bytes casten)

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
