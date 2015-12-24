import random

bucket_size = 4 # size of bucket

class node(object):
  def __init__(
    self,					#
    id = random.getrandbits(bucket_size),	# id of node (1 .. 1.048.575) as (20-) bitstring
    bucket = [[(0,0,0) for x in range(bucket_size)] for x in range(bucket_size)], # 
						# 20 buckets to store respectively 20 nodes
						# bucket[bucket-nr][list of (id,ip,port)]
						# niedriger Wert im Bucket = sehr nahe
						# hoher Wert im Bucket = weit entfernt
    keys = []					# known keys
  ):
    self.id = id
    self.bucket = bucket
    self.keys = keys

  # ID zu Bucket hinzufuegen (neue ID, neue IP, neuer Port)
  def bucket_add(self, n_id, n_ip, n_port):
    # (((x-or um Entfernung zu kennen) in binaer umwandeln) umso laenger die binaerzahl, umso weiter entfernt)
    # (laenge - 1) da Bucket-index mit 0 beginnt
    distance = len(bin(self.id ^ n_id))-3
    #print ("distance: ",str(distance))
    #print (self.id ^ n_id)
    for i in range(bucket_size):
      if self.bucket[distance][i][0] is 0:
        self.bucket[distance][i] = (n_id,n_ip,n_port)
        print ("einfuegen")
        break
      elif i is (bucket_size-1): # TODO ueberlauflisten hinzufuegen
        break
      else:
        continue
      
  def find_id(self, key):
    # search for key in known keys
    for i in range(len(self.keys)):
      if key is keys[i]:
        return keys[i]

    # key not known -> search in buckets
    distance = len(bin(self.id ^ key))-3
    returns = self.bucket[distance]
    if returns[(bucket_size-1)][0] is 0: # array ist nicht voll -> auffuellen
      for k in range(bucket_size):
        if returns[k][0] is 0:
          break
      i = distance - 1
      while i is not distance:
        #print("i: ",str(i)," distance: ",str(distance))
        for j in range(bucket_size):
          if self.bucket[i][j][0] is 0:
            break
          else:
            returns[k] = self.bucket[i][j]
            k += 1
            if k > (bucket_size-1): # if returns full
              return returns
        i -= 1
        if i < 0:
          i = (bucket_size-1)
      return returns # not enough known hosts to fill returns
          







