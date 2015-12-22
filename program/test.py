
import socket
import random


def test():
  id1 = random.getrandbits(4)
  id2 = random.getrandbits(4)
  print (id1)
  print (id2)
  id3 = (id1 ^ id2)
  print (id3)


test();
#test("open");
#connect();
#socket("open");
