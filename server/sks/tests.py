from django.test import TestCase
import threading
import queue


class DHTThread(threading.Thread):

    def __init__(self, ip, port):
        print("Init DHTThread")
        super(DHTThread, self).__init__()

        self.input_q = queue.Queue(1)
        self.output_q = queue.Queue(1)
        self.ip = ip
        self.port = port
        self.keys = {}

        print("DHTThread initialized.")

    def run(self):

        while True:

            print("Waiting for requests...")

            request = self.input_q.get()

            print("Processing request.")

            op = request[0]

            if op == 'get':
                print("Get key from DHT")
                pgp_key = self.get(request[1])

                # print("Retrieved key from DHT: " + str(pgp_key))
                self.output_q.put(pgp_key)

            elif op == 'put':
                key_id = request[1]
                key = request[2]

                # print("Put key with key_id: " + str(key_id) + " and data: " + str(key))

                self.put(key_id, key)

                self.output_q.put(0)

    def put(self, key, value):
        self.keys[key] = value

    def get(self, key):
        if key in self.keys:
            return self.keys[key]
        else:
            return None
