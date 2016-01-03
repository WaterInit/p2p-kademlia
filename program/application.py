import os.path
import pickle
import sys
from pgp import PGPKey, PGPEntry

file = 'temp/keys'

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
    pass
    #TODO


# insert <pgp_key> into DHT system
def insert_key(pgp_key):
    pass
    #TODO


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
if len(sys.argv) > 1:
    # init with new email address
    pgp_key = PGPKey(sys.argv[1])
    store_key(pgp_key)

else:
    # init with stored data
    pgp_key = load_key()
    assert pgp_key is not -1

print(pgp_key.pgp_entry)
