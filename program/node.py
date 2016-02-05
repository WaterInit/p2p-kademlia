import random
from threading import Thread
import threading
import socket
import pickle

bucket_size = 4  # size of bucket
alpha = 4  # number of simultaneous connections/Threads
# 0 = not in use, 1 = in use, 2 = finished
s_bucket = []


class node(object):
	def __init__(
					self,  #
					first_id,
					first_ip,
					first_port,
					myversion="1",  # version of this product
					myid=random.getrandbits(bucket_size),  # id of node (1 .. 1.048.575) as (20-) bitstring
					bucket=[[] for x in range(bucket_size)],  # 20 buckets to store respectively 20 nodes
					# bucket[bucket-nr][list of (id,ip,port)]
					# niedriger Wert im Bucket = sehr nahe
					# hoher Wert im Bucket = weit entfernt
					keys=[],  # known keys
					bucket_lock=threading.Lock(),  # lock bucket
					serveraddress=('0', 0),  # (server_ip, server_port)
	):
		self.myversion = myversion
		self.myid = myid
		self.bucket = bucket
		self.keys = keys
		self.bucket_lock = bucket_lock
		self.serveraddress = serveraddress
		self.listen_socket = self.server("open")  # listen socket
		self.thread_main = Thread(target=self.control, args=())
		self.thread_main.start()
		self.stoprequest = threading.Event()
		if not (first_ip is 0 and first_port is 0):
			self.bucket_add(int(first_id), first_ip, int(first_port))
			self.find_key(self.myid)

	# infinity wait for connections
	def control(self):
		while True:
			# print that the host is ready and wait for connection
			print ("start")
			# wait for Connection
			connection, client_address = self.listen_socket.accept()

			# get version and to do ###
			infos = pickle.loads(connection.recv(1024))
			version = infos[0]
			todo = infos[1]
			connection.sendall("0".encode())  # answer to distinguish bit-streams
			# get contact-information ###
			c_infos = pickle.loads(connection.recv(1024))  # Client (id,ip,port)
			connection.sendall("0".encode())  # answer to distinguish bit-streams
			self.bucket_add(c_infos[0], c_infos[1], c_infos[2])  # ID hinzufuegen

			# test case ###
			if int(todo) is 0:
				s_key = int(connection.recv(4).decode())  # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
				print ("erhaltene Daten: ", (s_key))  # test (erhaltene ID ausgeben)
				print (self.bucket)  # print complete bucket
			# Client is searching key. return key or clother hosts ###
			elif int(todo) is 1:  # test cases
				s_key = int(connection.recv(4).decode())  # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
				returns = self.find_id(s_key)
				connection.sendall(pickle.dumps(returns))  # serialize to send
			# Client want a is-life message
			elif int(todo) is 2:  #
				connection.sendall("1".encod())  # 1 = this host is alive
			# get unknown ID
			else:  # TODO maybe do something
				print ("error beim finden in main")

	# add ID to Bucket (new ID, new IP, new Port)
	def bucket_add(self, n_id, n_ip, n_port):
		# (((x-or um Entfernung zu kennen) in binaer umwandeln) umso laenger die binaerzahl, umso weiter entfernt)
		# (laenge - 1) da Bucket-index mit 0 beginnt
		distance = len(bin(self.myid ^ n_id)) - 3
		for i in range(len(self.bucket[distance])):  # ID already exist?
			if self.bucket[distance][i][0] is n_id:
				(self.bucket[distance]).append(self.bucket[distance].pop(i))
				print (self.bucket)
				return 0
		if len(self.bucket[distance]) < bucket_size:  # bucket not full, ID not existing
			(self.bucket[distance]).append((n_id, n_ip, n_port))
			print (self.bucket)
			return 0
		else:  # TODO ueberlaufliste hinzufuegen
			host = self.bucket[distance][0]
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
			client_socket.connect((host[1], host[2]))  # Verbindung zum Server aufbauen (ip,port)
			# send Version and to do
			client_socket.sendall(pickle.dumps([self.myversion, "2"]))
			if int(client_socket.recv(4).decode()) is 1:  # Server is alive
				(self.bucket[distance]).append(self.bucket[distance].pop(0))
			else:  # Server is down
				self.bucket[distance].pop(0)
				(self.bucket[distance]).append((n_id, n_ip, n_port))

			return 0

	# find key and return bucket with near IDs to the key ###
	# find local entrys only ###
	# first Step in search or return for another request
	def find_id(self, key):
		# TODO search for key in known keys
		for i in range(len(self.keys)):
			if key is keys[i]:
				return keys[i]
		# key unknown -> search in buckets
		distance = len(bin(self.myid ^ key)) - 3
		returns = self.bucket[distance][:]
		if key is self.myid:  # TODO find existing node at initialize, lt. Scheuermann=Absturz ist hier egal
			return 1  # return error
		if len(returns) < bucket_size:  # array ist nicht voll -> auffuellen
			backward = 0
			i = distance - 1
			if i < 0:
				backward = 1
				i = distance + 1
			while i < bucket_size:
				# print("i: ",str(i)," distance: ",str(distance))
				for j in range(len(self.bucket[i])):
					returns.append(self.bucket[i][j])
					if len(returns) is bucket_size:
						return returns  # Bucket is now full
				if backward is 0:  # go forward
					i -= 1
				else:  # go backward
					i += 1
				if i < 0:
					i = distance + 1
					backward = 1
		return returns  # Bucket is already full

	# distributet connects to other Hosts
	# (search key, using bucket, connecting Host
	def dist_connects(self, *args):
		s_key = args[0]
		host = args[1]
		global s_bucket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
		client_socket.connect((host[2], host[3]))  # Verbindung zum Server aufbauen (ip,port)

		# send Version and to do
		client_socket.sendall(pickle.dumps([self.myversion, "0001"]))
		if int(client_socket.recv(4).decode()) is not 0:  # Antwort senden um bit-stream zu unterscheiden
			print("Fehler")
			return 0

		# send own Server [id,ip,port]
		client_socket.sendall(pickle.dumps(
			[self.myid, self.serveraddress[0], self.serveraddress[1]]))  # ID senden und encoden (in bytes casten)
		if int(client_socket.recv(4).decode()) is not 0:  # Antwort senden um bit-stream zu unterscheiden
			print("Fehler")
			return 0

		# send key
		client_socket.sendall(str(s_key).encode())
		# wait for answer
		mybucket = pickle.loads(client_socket.recv(1024))
		# print("mybucket: ",str(mybucket))
		# insert into bucket
		for i in range(len(mybucket)):
			if mybucket[i][0] is not self.myid:  # check if Bucket own one, if not -> add
				self.bucket_add(int(mybucket[i][0]), mybucket[i][1], int(mybucket[i][2]))
		self.bucket_lock.acquire()
		# print(mybucket)
		for i in range(len(s_bucket)):  # change Host to done
			if s_bucket[i][1] is host[1]:
				s_bucket[i] = (2,) + s_bucket[i][1:]  # does following: "s_bucket[i][0] = 2"
				# print("3: ",str(s_bucket))
				break
		# if s_bucket not full append new Hosts
		while ((len(s_bucket)) < bucket_size) and ((len(mybucket)) > 0):
			for i in range(len(mybucket)):
				already_in = 0
				for k in range(len(s_bucket)):  # check if Host already in
					if (s_bucket[k][1] is mybucket[i][0]) or (mybucket[i][0] is self.myid):
						already_in = 1
						break
				if already_in is 0:
					# (new host - not used, id, ip, port)
					s_bucket.append((0, mybucket[i][0], mybucket[i][1], mybucket[i][2]))
				mybucket.pop(i)
				break
		# if s_bucket is full replace Hosts
		if (len(mybucket)) > 0:
			for i in range(len(s_bucket)):
				distance = (s_bucket[i][1] ^ s_key)
				for j in range(len(mybucket)):
					if (mybucket[j][0] ^ s_key) < distance:  # new Host is closer
						already_in = 0
						for k in range(len(s_bucket)):  # check if Host already in
							if (s_bucket[k][1] is mybucket[j][0]) or (mybucket[j][0] is self.myid):
								already_in = 1
								break
						if already_in is 0:
							s_bucket[i] = (0, mybucket[j][0], mybucket[j][1], mybucket[j][2])
							# s_bucket[i][0] = 0 # new Host not used
							# s_bucket[i][1] = mybucket[j][0] # id
							# s_bucket[i][2] = mybucket[j][1] # ip
							# s_bucket[i][3] = mybucket[j][2] # port
						mybucket.pop(j)
						break
		self.bucket_lock.release()

	# find key in network ###
	def find_key(self, s_key):
		global s_bucket
		if s_key is self.myid:  # only at initialize
			for i in range(bucket_size):
				if len(self.bucket[i]) > 0:
					mybucket = self.bucket[i][:]
					break
		else:
			mybucket = self.find_id(s_key)[:]

		s_bucket = []  # save hosts with bit of sending here
		threads = []  # save threads here
		while len(mybucket) > 0:
			buck = mybucket.pop()
			s_bucket.append((0, buck[0], buck[1], buck[2]))  # (0 = not using, id, ip, port)
		# manage threads ###
		while True:
			active = 0  # number of active threads
			done = 0  # number of finished threads
			self.bucket_lock.acquire()  # threadsafe from here
			for i in range(len(s_bucket)):
				if s_bucket[i][0] is 1:  # Host connected
					active += 1
				elif s_bucket[i][0] is 2:  # Host finished
					done += 1
			# print("active: ",str(active)," done: ",str(done)," all: ",str(len(s_bucket)),"\n bucket: ",str(s_bucket))
			# warte = input("wait")
			if done is len(s_bucket):  # finished
				break
			# start new thread
			if (active < alpha) and ((active + done) < len(s_bucket)):
				# choose Host for new connection
				mem_j = 0
				for j in range(len(s_bucket)):
					mem_j = j
					if s_bucket[j][0] is 0:  # found new Host
						# does following in a list "s_bucket[j][0] = 1"
						s_bucket[j] = (1,) + s_bucket[j][1:]  # set to "in use"
						break
				threads.append(Thread(target=self.dist_connects, args=(s_key, s_bucket[mem_j])))
				threads[len(threads) - 1].start()
			self.bucket_lock.release()  # threadsafe until here
			# ready

	# Server definieren, socket oeffnen
	def server(self, *todo):  # first arg = what to do, second arg = optional socket-object
		server_address = (socket.gethostname(), 0)
		if todo[0] is 'open':
			# print ("laeuft") # testen (server gestartet)
			listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
			listen_socket.bind(server_address)  # socket an IP und Port binden
			listen_socket.listen(5)  # socket als listen definieren
			# print (listen_socket.getsockname())
			self.serveraddress = listen_socket.getsockname()
			return listen_socket

		elif todo[0] is 'close':
			todo[1].close()
			print ("socket schliessen")
		else:
			print ("nichts")

	# some actions (like "stop server")
	def action(self, aktion):
		if aktion == 'stop':  # stop server
			# stop listen thread
			# self.thread_main.cancel()
			# stop listen socket
			self.server("close", self.listen_socket)
			return 1
