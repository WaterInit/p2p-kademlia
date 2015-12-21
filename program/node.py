import random

class node(object):
  def __init__(
    self,							# inititalizing
    id = format(random.getrandbits(20), '020b'),		# id of node (1 .. 1.048.575) as bitstring
    bucket = [[(0,0,0) for x in range(20)] for x in range(20)]	# 20 buckets to store respectively 20 nodes
								# bucket[bucket-nr][(id,ip,port)]
  ):
    self.id = id
    self.bucket = bucket
