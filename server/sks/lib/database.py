import queue
from . import gpg, DHTThread
from .. import tests

# INIT
# parse config file
config_name = 'config'
parameters = {}

with open(config_name, 'r') as config_file:
    lines = config_file.readlines()

for line in lines:
    if line.startswith('#') or line.startswith(' '):
        continue
    else:
        key, value = line.partition('=')[::2]
        parameters[key.rstrip()] = value.rstrip()

# print(parameters)

# create DHT thread
dht_thread = DHTThread.DHTThread(str(parameters['bootstrap_ip']), parameters['bootstrap_port'])
dht_thread.start()

thread_input_q = dht_thread.input_q
thread_output_q = dht_thread.output_q

temp_file = 'temp_file.asc'

print("database ready")

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

    print("Exit code: " + str(code))

    return code


# convenient getters
def get_metadata(key_id):

    thread_input_q.put(['get', key_id])
    key = thread_output_q.get()

    info = None

    if key is not None:
        info = (gpg.get_info(temp_file))[0]

    return info

