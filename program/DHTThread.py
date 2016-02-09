#!/usr/bin/python3

#from django.test import TestCase
import threading
import queue
from node import node



class DHTThread(threading.Thread):

	def __init__(self, ip, port):
		print("Init DHTThread")
		super(DHTThread, self).__init__()

		self.input_q = queue.Queue(1)
		self.output_q = queue.Queue(1)
		self.ip = ip
		self.port = port

		self.knoten = node(self.ip, self.port)
		print("DHTThread initialized.")
		self.run()

	def run(self):
		while True:
			print("Waiting for requests...")
			#key = self.input_q.get()
			key = input("")
			print("Processing request.")

			if key[0] == "put":  # insert in DHT
				pgp_entry = self.knoten.insert_key(key[1], key[2])
				self.output_q.put(pgp_entry)
			elif key[0] == "get":  # get from DHT
				pgp_entry = self.knoten.get_key(key[1])
				if pgp_entry is 0:  # key not found
					self.output_q.put(None)
				else:
					self.output_q.put(pgp_entry)
			else:
				self.output_q.put(None)