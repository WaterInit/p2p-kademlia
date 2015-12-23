import random

class node(object):
  def __init__(
    self,							# inititalizing
    id = random.getrandbits(20),				# id of node (1 .. 1.048.575) as bitstring
    bucket = [[(0,0,0) for x in range(20)] for x in range(20)]	# 20 buckets to store respectively 20 nodes
								# bucket[bucket-nr][(id,ip,port)]
  ):
    self.id = id
    self.bucket = bucket

  # ID hinzufuegen (neue ID, neue IP, neuer Port)
  def bucket_add(n_id,n_ip,n_port):
     # (((x-or um Entfernung zu kennen) in binaer umwandeln) umso laenger die binaerzahl, umso weiter entfernt)
    distance = len(bin((self.id ^ n_id)))
      
      
