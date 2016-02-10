import random
from threading import Thread
import threading
import socket
import pickle
import hashlib
import binascii
import sys


bucket_size = 40  # size of bucket
bucket_width = 20
alpha = 4  # number of simultaneous connections/Threads
# 0 = not in use, 1 = in use, 2 = finished
s_bucket = []
key_list = []


class node(object):
	def __init__(
					self,  #
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
		# start thread for incoming Messages from another node
		self.thread_main = Thread(target=self.control, args=())
		self.thread_main.start()
		# start thread for input from application
		self.thread_action = Thread(target=self.action, args=())
		self.thread_action.start()
		self.stoprequest = threading.Event()
		if int(first_port) != 0:
			self.find_key(self.myid, first_ip, first_port)
		print(self.myid, self.listen_socket.getsockname()[0], self.listen_socket.getsockname()[1])

	# infinity wait for connections
	def control(self):
		while True:
			# print that the host is ready and wait for connection
			# wait for Connection
			print("ready")
			connection, client_address = self.listen_socket.accept()

			# get version and to do ###
			infos = pickle.loads(connection.recv(1024))
			version = infos[0]
			todo = infos[1]
			if int(todo) is 2:  # check if Host is alive
				connection.sendall("1".encode())  # 1 = this host is alive
				continue
			elif int(todo) is 3:  # needs id only
				connection.sendall(str(self.myid).encode())
				continue
			elif int(todo) is 4:  # get new key entry
				'''
				connection.sendall("1".encode())  # give key
				new_key = pickle.loads(connection.recv(1024))  # key (key_id,value)
				self.key_add(new_key[0], new_key[1])
				continue
				'''
				connection.sendall("1".encode())  # give key
				#input_length = pickle.loads(connection.recv(1024))
				#connection.sendall("1".encode())  # give key
				#print("input_length: "+str(input_length))
				new_key2 = b''
				d = True
				l = 100
				while d:
					d = (connection.recv(8192))  # key (key_id,value)
					new_key2 += d
				new_key = pickle.loads(new_key2)
				#print("DEBUG: new_key: "+str(new_key))
				self.key_add(new_key[0], new_key[1])
				continue


			connection.sendall("0".encode())  # answer to distinguish bit-streams
			# get contact-information ###
			c_infos = pickle.loads(connection.recv(1024))  # Client (id,ip,port)
			connection.sendall("0".encode())  # answer to distinguish bit-streams

			# test case ###
			if int(todo) is 0:
				s_key = int(connection.recv(4).decode())  # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
				#print ("erhaltene Daten: ", s_key)  # test (erhaltene ID ausgeben)
				print (self.bucket)  # print complete bucket
			# Client is searching key. return key or clother hosts ###
			elif int(todo) is 1:
				s_key = int(connection.recv(1024).decode())  # erhalte 20 Bytes (20-stellige ID des keys) und decode diese
				#print("DEBUG: "+str(s_key))
				returns = self.find_id(s_key)
				#print("DEBUG key: "+str(s_key))
				#print("DEBUG returns: "+str(returns))
				#print("DEBUG pickle-return: "+str(pickle.dumps(returns)))
				connection.sendall(pickle.dumps(returns))  # serialize to send
				#print("DEBUG done")
			else:  # get unknown to_do # TODO maybe do something
				print ("received unknown todo from another Host")

			# add Host to local Bucket
			self.bucket_add(c_infos[0], client_address[0], c_infos[2])  # ID hinzufuegen

	# add key into DHT
	def insert_key(self, key, value):
		# id of the key in DHT (key to 20-bit id)
		key_id = (int((hashlib.sha1(key.encode())).hexdigest(), 16) % (2**bucket_size))
		# find 20 clothest Hosts
		hosts = self.find_id(key_id)
		# check if i'm one of the 20 clothest hosts (only if there another host)
		if len(hosts) < bucket_size:
			self.key_add(key_id, value)  # add key in my own list
		else:
			far_away = 0
			for i in range(1, len(hosts)):
				if (hosts[i][0] ^ key_id) > (hosts[far_away][0] ^ key_id):
					far_away = i
			if (self.myid ^ key_id) > (hosts[far_away][0] ^ key_id): # im clother then another host
				hosts.pop(far_away)  # remove farthest host from list
				#self.key_add(key_id, value)  # add key in my own list
		# add key to all hosts
		for i in range(len(hosts)):
			try:
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
				socket.timeout(8)
				client_socket.connect((hosts[i][1], hosts[i][2]))  # Verbindung zum Server aufbauen (ip,port)
				# send Version and to do
				client_socket.sendall(pickle.dumps([self.myversion, "4"]))
				if int(client_socket.recv(4).decode()) is not 1:  # Antwort senden um bit-stream zu unterscheiden
					print("Fehler")
					return 0
				# send key [key_id,value]
				client_socket.sendall(pickle.dumps([key_id, value]))  # ID senden und encoden (in bytes casten)
			except:  # not able to connect to socket
				# nothing to do

				continue
		return 0

	# add key in my key-list
	def key_add(self, key, value):
		# check if key already in list
		for i in range(len(self.keys)):
			if self.keys[i][0] == key:
				return 0
		self.keys.append((key, value))
		print ("keys: "+str(self.keys))

	# add ID to Bucket (new ID, new IP, new Port)
	def bucket_add(self, n_id, n_ip, n_port):
		# check, if id own id
		if n_id == self.myid:
			return 0
		# (((x-or um Entfernung zu kennen) in binaer umwandeln) umso laenger die binaerzahl, umso weiter entfernt)
		# (laenge - 1) da Bucket-index mit 0 beginnt
		distance = len(bin(self.myid ^ n_id)) - 3
		for i in range(len(self.bucket[distance])):  # ID already exist?
			if self.bucket[distance][i][0] == n_id:
				#(self.bucket[distance]).append(self.bucket[distance].pop(i))
				# print ("Host alrady exist")
				return 0
		if len(self.bucket[distance]) < bucket_width:  # bucket not full, ID not existing
			(self.bucket[distance]).append((n_id, n_ip, n_port))
			print (self.bucket)
			return 0
		else:  # ueberlaufliste (Warteschlange)
			host = self.bucket[distance][0]
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
			client_socket.settimeout(8)  # set timeout 8 sec
			try:
				client_socket.connect((host[1], host[2]))  # Verbindung zum Server aufbauen (ip,port)
			except socket.timeout:  # Server is down
				self.bucket[distance].pop(0)
				(self.bucket[distance]).append((n_id, n_ip, n_port))
				return 0
			# send Version and to do
			client_socket.sendall(pickle.dumps([self.myversion, "2"]))
			if int(client_socket.recv(4).decode()) is 1:  # Server is alive
				(self.bucket[distance]).append(self.bucket[distance].pop(0))
			else:  # Server is down
				self.bucket[distance].pop(0)
				(self.bucket[distance]).append((n_id, n_ip, n_port))

			return 0

	# find key and return bucket with clothest Hosts to the key ###
	# find local entrys only
	# first Step in search or return for another request
	def find_id(self, key):
		# search for key in known keys
		for i in range(len(self.keys)):
			if key == self.keys[i][0]:
				return self.keys[i][:]
		# key unknown -> search in buckets
		distance = len(bin(self.myid ^ key)) - 3
		returns = self.bucket[distance][:]
		if key is self.myid:  # to_do find existing node at initialize, lt. Scheuermann=Absturz ist hier egal
			return 0  # return error
		if len(returns) < bucket_size:  # array ist nicht voll -> auffuellen
			backward = 0
			i = distance - 1
			if i < 0:
				backward = 1
				i = distance + 1
			while i < bucket_size:
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
	# (search key, using bucket, connecting Host)
	def dist_connects(self, *args):
		global key_list
		s_key = args[0]
		host = args[1]
		key_list = args[2]
		mybucket = ()
		global s_bucket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
		socket.timeout(8)
		connection_success = 1  # if connection is successed
		new_key2 = b''
		try:
			client_socket.connect((host[2], host[3]))  # Verbindung zum Server aufbauen (ip,port)
			# send Version and to do
			client_socket.sendall(pickle.dumps([self.myversion, "1"]))
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
			d = True
			l = 100
			client_socket.settimeout(1)
			while d:
				d = (client_socket.recv(1024))  # key (key_id,value)
				new_key2 += d
				#print("DEBUG data: "+str(new_key2))
			mybucket = pickle.loads(new_key2)
			#print("DEBUG mybucket: "+str(mybucket))

		except socket.timeout:
			mybucket = pickle.loads(new_key2)
			#print("DEBUG mybucket: "+str(mybucket))

		except:  # not able to connect to socket
			# delete host from bucket
			self.bucket_lock.acquire()
			distance = len(bin(self.myid ^ host[1])) - 3
			for i in range(len(self.bucket[distance])):  # ID already exist?
				if self.bucket[distance][i][0] is host[1]:
					self.bucket[distance].pop(i)
					print (self.bucket)
					break
			# delete Host from searching list
			for i in range(len(s_bucket)):
				if s_bucket[i][1] is host[1]:
					s_bucket.pop(i)
					break
			self.bucket_lock.release()
			connection_success = 0

		if connection_success is 1:
			# check if answer is a key or bucket
			#if len(mybucket) is 2:  # got the key
			#print("DEBUG bis hier")
			# TODO checken ob liste und wie groß (Ausgabe) usw.
			if len(mybucket) is 2 and isinstance(mybucket[1], str):
				#print("DBEUG klappt")
				key_list.append(mybucket)
				return 0
			# got a Bucket - no key
			# insert into bucket
			#print("DEBUG mybucket before: "+str(mybucket))
			for i in range(len(mybucket)):
				if mybucket[i][0] is not self.myid:  # check if Bucket own one, if not -> add
						self.bucket_add(int(mybucket[i][0]), mybucket[i][1], int(mybucket[i][2]))
		self.bucket_lock.acquire()
		for i in range(len(s_bucket)):  # change Host to done
			if s_bucket[i][1] is host[1]:
				s_bucket[i] = (2,) + s_bucket[i][1:]  # does following: "s_bucket[i][0] = 2"
				break
		if connection_success is 1:
			# if s_bucket not full append new Hosts
			while ((len(s_bucket)) < bucket_size) and ((len(mybucket)) > 0):
				for i in range(len(mybucket)):
					already_in = 0
					for k in range(len(s_bucket)):  # check if Host already in
						if (s_bucket[k][1] == mybucket[i][0]) or (mybucket[i][0] == self.myid):
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
								# new Host - not used, id, ip, port
								s_bucket[i] = (0, mybucket[j][0], mybucket[j][1], mybucket[j][2])
							mybucket.pop(j)
							break
		self.bucket_lock.release()

	def get_key(self, key):
		key_id = (int((hashlib.sha1(key.encode())).hexdigest(), 16) % (2**bucket_size))
		ret = self.find_key(key_id)
		if ret is not 0:  # key found
			return ret
		else:  # key not found
			return 0

	# find key in network ###
	def find_key(self, s_key, *first):
		global s_bucket
		global key_list
		# initialize only
		# first[0] = init_ip
		# first[1] = init_port
		if s_key is self.myid:  # only at initialize
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
			client_socket.connect((first[0], int(first[1])))  # Verbindung zum Server aufbauen (ip,port)

			client_socket.sendall(pickle.dumps([self.myversion, "3"]))
			first_id = int(client_socket.recv(1024).decode())
			self.bucket_add(int(first_id), first[0], int(first[1]))
			for i in range(bucket_size):
				if len(self.bucket[i]) > 0:
					mybucket = self.bucket[i][:]
					break
		else:
			mybucket = self.find_id(s_key)[:]  # get local known clothest Hosts
			# found key? -> len(mybucket) = 2 (only id and value) and mybucket[0] is int (id of key)
			if len(mybucket) is 2 and isinstance(mybucket[0], int):
				return mybucket[1]
		s_bucket = []  # save hosts with bit of sending here
		key_list = []  # save key, if any found
		threads = []  # save threads here
		ret = 0
		while len(mybucket) > 0:
			buck = mybucket.pop()
			s_bucket.append((0, buck[0], buck[1], buck[2]))  # (0 = not active, id, ip, port)
		# manage threads ###
		while True and len(s_bucket) > 0:
			active = 0  # number of active threads
			done = 0  # number of finished threads
			if not len(key_list) is 0:  # found key (entry in key_list)
				return key_list[0][1]  # return only value of the key
			self.bucket_lock.acquire()  # threadsafe from here
			for i in range(len(s_bucket)):
				if s_bucket[i][0] is 1:  # Host connected
					active += 1
				elif s_bucket[i][0] is 2:  # Host finished
					done += 1
			if done >= len(s_bucket):  # finished
				self.bucket_lock.release()  # threadsafe until here
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
				threads.append(Thread(target=self.dist_connects, args=(s_key, s_bucket[mem_j], key_list)))
				threads[len(threads) - 1].start()
			# ready
			self.bucket_lock.release()  # threadsafe until here
		return ret

	# Server definieren, socket oeffnen
	def server(self, *todo):  # first arg = what to do, second arg = optional socket-object
		server_address = (socket.gethostname(), 0)
		if todo[0] is 'open':
			listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialisieren
			listen_socket.bind(('', 0))  # socket an IP und Port binden
			listen_socket.listen(5)  # socket als listen definieren
			self.serveraddress = listen_socket.getsockname()
			return listen_socket

		elif todo[0] is 'close':
			todo[1].close()
			print ("socket schliessen")
		else:
			print ("nichts")

	# some actions (like "stop server")
	def action(self):
		while True:
			user_todo = input("")
			if user_todo == "put":
				key = input("")
				self.insert_key(key, key)
			elif user_todo == "get":
				key = input("")
				ret = self.get_key(key)
				print(ret)
			else:
				print (user_todo)
