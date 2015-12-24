import random

bucket_size = 4 # size of bucket

class node(object):
  def __init__(
    self,					#
    myid = random.getrandbits(bucket_size),	# id of node (1 .. 1.048.575) as (20-) bitstring
    bucket = [[(0,0,0) for x in range(bucket_size)] for x in range(bucket_size)], # 
						# 20 buckets to store respectively 20 nodes
						# bucket[bucket-nr][list of (id,ip,port)]
						# niedriger Wert im Bucket = sehr nahe
						# hoher Wert im Bucket = weit entfernt
    keys = []					# known keys
  ):
    self.myid = myid
    self.bucket = bucket
    self.keys = keys

  # ID zu Bucket hinzufuegen (neue ID, neue IP, neuer Port)
  def bucket_add(self, n_id, n_ip, n_port):
    # (((x-or um Entfernung zu kennen) in binaer umwandeln) umso laenger die binaerzahl, umso weiter entfernt)
    # (laenge - 1) da Bucket-index mit 0 beginnt
    distance = len(bin(self.myid ^ n_id))-3
    #print ("distance: ",str(distance))
    #print (self.myid ^ n_id)
    for i in range(bucket_size):
      #print(self.myid,n_id,distance,i)
      if self.bucket[distance][i][1] is 0: # empty slot, id can be 0 - ip cant be 0
        self.bucket[distance][i] = (n_id,n_ip,n_port)
        #print ("einfuegen")
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
    distance = len(bin(self.myid ^ key))-3
    returns = self.bucket[distance]
    if key is self.myid:
      return returns
    if returns[(bucket_size-1)][1] is 0: # array ist nicht voll -> auffuellen
      k = 0
      while returns[k][1] is not 0:
        k += 1
      i = distance - 1
      while i is not distance:
        #print("i: ",str(i)," distance: ",str(distance))
        for j in range(bucket_size):
          print ("blub: ",str(j),str(k))
          if self.bucket[i][j][1] is 0:
            break
          else:
            '''
            print (self.bucket[i][j])
            returns[k] = self.bucket[i][j]
            k += 1
            if k > (bucket_size-1): # if returns full
              return returns
            '''
        i -= 1
        if i < 0:
          i = (bucket_size-1)
      return returns # not enough known hosts to fill returns
    return returns # Bucket is already full
          







