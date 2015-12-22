import random

class node(object):
  def __init__(
    self,							# inititalizing
    id = random.getrandbits(20),				# id of node (1 .. 1.048.575) as bitstring
    bucket = [[(0,0,0) for x in range(20)] for x in range(20)]	# 20 buckets to store respectively 20 nodes
								# bucket[bucket-nr][(id,ip,port)]
  ):
    self.id = ide
    self.bucket = bucket

  # ID hinzufuegen (add), finden
  def bucket(todo,s_id):
    if todo is 'add':
      distance = (self.id ^ s_id)
      
      
