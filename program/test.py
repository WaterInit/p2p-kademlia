import socket

def server():
  while True:
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((socket.gethostname(), 80))
    listen_socket.listen(5)


server();
