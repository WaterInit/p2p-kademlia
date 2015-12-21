
import socket

def socket(todo):
  if todo is 'open':
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((socket.gethostname(), 80))
    listen_socket.listen(1)


def connect():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(("www.python.org",80))

def test(todo):
  #if todo is 'open':
  if 'open' in todo:
    print ("initialisieren")
  elif todo is 'close':
    print ("close it")
  else:
    print ("else it")


#test("open");
connect();
#socket("open");
