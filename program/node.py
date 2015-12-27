import random

bucket_size = 4 # size of bucket

class node(object):
  def __init__(
    self,					#
    myid = random.getrandbits(bucket_size),	# id of node (1 .. 1.048.575) as (20-) bitstring
    bucket = [[] for x in range(bucket_size)],	# 20 buckets to store respectively 20 nodes
						# bucket[bucket-nr][list of (id,ip,port)]
						# niedriger Wert im Bucket = sehr nahe
						# hoher Wert im Bucket = weit entfernt
    keys = []					# known keys
  ):
    self.myid = myid
    self.bucket = bucket
    self.keys = keys


  ### add ID to Bucket (new ID, new IP, new Port)
  def bucket_add(self, n_id, n_ip, n_port):
    # (((x-or um Entfernung zu kennen) in binaer umwandeln) umso laenger die binaerzahl, umso weiter entfernt)
    # (laenge - 1) da Bucket-index mit 0 beginnt
    distance = len(bin(self.myid ^ n_id))-3
    for i in range(len(self.bucket[distance])): # ID already exist?
      if self.bucket[distance][i][0] is n_id:
        (self.bucket[distance]).append(self.bucket[distance].pop(i))
        return 0
    if len(self.bucket[distance]) < bucket_size: # bucket not full, ID not existing
      (self.bucket[distance]).append((n_id,n_ip,n_port))
      return 0
    else: # TODO ueberlaufliste hinzufuegen
      return 0



  ### find key and return bucket with near IDs to the key ###
  def find_id(self, key):
    # TODO search for key in known keys
    for i in range(len(self.keys)):
      if key is keys[i]:
        return keys[i]
    # key not known -> search in buckets
    distance = len(bin(self.myid ^ key))-3
    returns = self.bucket[distance][:]
    if key is self.myid: # TODO find existing node at initialize, lt. Scheuermann=Absturz ist hier egal
      return 1 # return error
    if len(returns) < bucket_size: # array ist nicht voll -> auffuellen
      i = distance - 1
      if i < 0:
        i = (bucket_size-1)
      while i is not distance:
        #print("i: ",str(i)," distance: ",str(distance))
        for j in range(len(self.bucket[i])):
          returns.append(self.bucket[i][j])
          if len(returns) is bucket_size:
            return returns # Bucket is now full
        i -= 1
        if i < 0:
          i = (bucket_size-1)
    return returns # Bucket is already full
          







