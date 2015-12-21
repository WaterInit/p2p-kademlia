import socket
import sys

server_address = (socket.gethostname(), 1240)

def server(todo):
  if todo is 'open':
    print ("laeuft")
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(server_address)
    listen_socket.listen(5)

    while True:
      connection, client_address = listen_socket.accept()
      print ("got it")
      data = connection.recv(20).decode()
      print ("erhaltene Daten: ",repr(data))




  elif todo is 'close':
    print ("stop it")

  else:
    print ("nichts")


def client(todo):
  if todo is 'connect':
    message = '11001001100010011011'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    client_socket.sendall(message.encode())

    print ("Client is done")
  else:
    print ("fehler am Client")


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
