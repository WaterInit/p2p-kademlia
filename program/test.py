
import socket
import random
import time # Threading test
from threading import Thread
import threading


def test(): # get random Bits
  id1 = random.getrandbits(4)
  id2 = random.getrandbits(4)
  print (str(id1)," ",len(bin(id1))-2," ",str(bin(id1)))
  print (str(id2)," ",len(bin(id2))-2," ",str(bin(id2)))
  id3 = (id1 ^ id2)
  print (str(id3)," ",len(bin(id3))-2," ",str(bin(id3)))

def test2(): # lists in arrays
  bucket = [[] for x in range(4)]
  print (bucket)
  (bucket[0]).append((1,2,3))
  (bucket[0]).append((4,5,6))
  (bucket[0]).append((7,8,9))
  print (bucket)
  bucket[0].append(bucket[0].pop(1))
  print (bucket)


def sleep(*i):
  print (i[2])
  time.sleep(int(1))
  print("fertig")

def test3(): # Threading
  for i in range(2):
    (Thread(target=sleep,args=((1,2,3)))).start()
  print (i)

#mylock = threading.Lock()

def sleep2():
  mylock.acquire()
  print ("start")
  time.sleep(5)
  print ("fertig")
  mylock.release()
def test4(): # locking
  t = Thread(target=sleep2,args=())
  t.start()
  time.sleep(1)
  mylock.acquire()
  print ("fertig2")


def test5_1(i):
  i.append(1)
def test5(): # call by reference
  i = []
  test5_1(i);
  test5_1(i);
  test5_1(i);
  test5_1(i);
  time.sleep(1)
  i.append(2)
  print (i)


def test6(): # ip,port,...
  print (socket.gethostname())
  #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket initialisieren
  #client_socket.connect(server_address) # Verbindung zum Server aufbauen

def test7(): # tuple
  l = (6,7,8,9)
  print (l)
  
  l = (1,)+l[1:]

  print (l)
  


test7();
#test6();
#test5();
#test4();
#test3();
#test2();
#test("open");
#connect();
#socket("open");
