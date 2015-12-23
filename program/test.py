
import socket
import random


def test():
  id1 = random.getrandbits(4)
  id2 = random.getrandbits(4)
  print (str(id1)," ",len(bin(id1))-2," ",str(bin(id1)))
  print (str(id2)," ",len(bin(id2))-2," ",str(bin(id2)))
  id3 = (id1 ^ id2)
  print (str(id3)," ",len(bin(id3))-2," ",str(bin(id3)))

def test2():
  bucket = [[(0,0,0) for x in range(4)] for x in range(4)]
  print (bucket[0][0][0])


test2();
#test("open");
#connect();
#socket("open");
