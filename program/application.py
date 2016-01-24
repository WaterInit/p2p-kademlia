import os.path
import pickle
import queue
from pgp import PGPKey, PGPEntry

file = 'temp/keys'
dht_thread = None

thread_input_q = queue.Queue(1)
thread_output_q = queue.Queue(1)

own_key = None


# LOCAL
def load_key():
    if os.path.exists(file):
        with open(file, 'rb') as input:
            data = pickle.load(input)
        return data
    else:
        return -1


def store_key(pgp_key):
    with open(file, 'wb') as output:
        pickle.dump(pgp_key, output)


# REMOTE
# get pgp key identified by <email>
def get_key(email):
    thread_input_q.put(['get', email])
    pgp_entry = thread_output_q.get()
    return pgp_entry


# insert <pgp_key> into DHT system
def insert_key(pgp_key):
    thread_input_q.put(['put', pgp_key])
    code = thread_output_q.get()
    return code


# sign key identified by <email> using own <pgp_key>
def sign_key(pgp_key, email):
    key = get_key(email)
    if key:
        key.sign(pgp_key.email, pgp_key.sec)
        insert_key(key)
    else:
        print("Error: Key not available!")
        return -1

# INIT
# create DHT thread
dht_thread = DHTThread(thread_input_q, thread_output_q)

# UI
while True:
    mode = int(input("Please choose: create key (0), get key (1) or sign key (3). > "))

    if mode == 0:
        email = input("Insert email address for new key. > ")

        # check if already exists
        pgp_entry = get_key(email)

        if pgp_entry is not None:
            print("PGPKey with given email address already exists!")
        else:
            # create new key
            key = PGPKey(email)
            print("Your PGPKey has been created successfully: " + str(key.pgp_entry))

            # save key in DHT
            code = insert_key(key.pgp_entry)
            if code == 200:
                print("Your PGPKey has been submitted to the system.")
                own_key = key
            else:
                print("An error occurred. Please contact your administrator.")

        break
    elif mode == 1:
        email = input("Insert email address. > ")

        # load key from DHT
        pgp_entry = get_key(email)

        if pgp_entry is not None:
            print(pgp_entry)
        else:
            print("Key with given email address not found.")

        break

    elif mode == 2:
        email = input("Insert signee email address. > ")

        # load key from DHT
        code = sign_key(own_key, email)

        if code == 200:
            signed_key = get_key(email)
            print("Signed key successfully: " + str(signed_key))
        else:
            print("An error occurred. Please contact your administrator.")

        break
    else:
        print("Invalid input")
