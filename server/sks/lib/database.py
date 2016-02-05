import Queue
from . import gpg
from .. import tests

# INIT
# create DHT thread
dht_thread = tests.DHTThread()
dht_thread.start()

thread_input_q = dht_thread.input_q
thread_output_q = dht_thread.output_q

temp_file = 'temp_file.asc'


# DHT ACCESS
# get pgp key identified by <id>
def get_key(key_id):

    thread_input_q.put(['get', key_id])
    key = thread_output_q.get()

    return key


# insert <key> into DHT system
def insert_key(key):

    with open(temp_file, 'w') as file:
        file.write(key)

    key_id = gpg.get_id(temp_file)

    thread_input_q.put(['put', key_id, key])
    code = thread_output_q.get()

    return code


# convenient getters
def get_metadata(key_id):

    thread_input_q.put(['get', key_id])
    key = thread_output_q.get()

    info = None

    if key is not None:
        info = (gpg.get_info(temp_file))[0]

    return info

