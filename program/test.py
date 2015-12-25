
import socket
import random
import time # Threading test
from threading import Thread


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


def sleep():
  time.sleep(5)
  print("fertig")

def test3(): # Threading
  threads = []
  for i in range(2):
    threads.append(Thread(target=sleep,args=()))
  for j in range(2):
    threads[j].start()
#  t2 = Thread(target=sleep,args=())
#  t2.start()
  print ("something")






test3();
#test2();
#test("open");
#connect();
#socket("open");
