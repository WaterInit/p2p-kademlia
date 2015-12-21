import socket
import sys
from node import node

server_address = (socket.gethostname(), 1240)

# Server definieren
def server(todo):
  knoten = node()
  print (knoten.id)
  print (len(knoten.id))
  if todo is 'open':
    print ("laeuft") # testen (server gestartet)
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
    listen_socket.bind(server_address) # socket an IP und Port binden
    listen_socket.listen(5) # socket als listen definieren

    while True:
      connection, client_address = listen_socket.accept() # auf Verbindung warten
      print ("got it") # testen (Verbindung aufgebaut)
      data = connection.recv(20).decode() # erhalte 20 Bytes (20-stellige ID) und decode diese
      print ("erhaltene Daten: ",repr(data)) # test (erhaltene ID ausgeben)

  ##### sinnloser Stuss Anfang #####
  elif todo is 'close':
    print ("stop it")
  else:
    print ("nichts")
  ##### sinnloser Stuss Ende #####

# Client definieren
def client(todo):
  if todo is 'connect':
    message = '11001001100010011011' # simbolisiert die ID

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
    client_socket.connect(server_address) # Verbindung zum Server aufbauen

    client_socket.sendall(message.encode()) # ID senden und encoden (in bytes casten)

    print ("Client is done") # test (fertig)
  ##### 2 Zeilen sinnloser Stuss #####
  else:
    print ("fehler am Client")


### ###
### entweder den Client oder den Server starten ###
### python3 main.py server
### python3 main.py client
### ###
def start_all():
  #if str(sys.argv[1]) is 'server':
  if 'server' in str(sys.argv[1]):
    server("open");
  elif 'client' in sys.argv[1]:
    client("connect");
  else:
    print ("Fehler beim Start")
    print (str(sys.argv[1]))


start_all();
