import gnupg
import subprocess
import wget
import os
from . import database

temp_dir = 'temp'
temp_dir_path = str(subprocess.getoutput(['pwd']).rstrip()) + '/' + temp_dir

download_dir = temp_dir + '/download'
ascii_dir = temp_dir + '/ascii'

# create temp directory if not already existing
if not os.path.exists(temp_dir):
    print("Create TEMP directory")
    os.makedirs(temp_dir)

    print("Create DOWNLOAD directory")
    os.makedirs(download_dir)

    print("Create ASCII directory")
    os.makedirs(ascii_dir)

# download dump files if necessary
url = 'http://keyserver.mattrude.com/dump/2016-02-07/'

for i in range(1):
    file_name = 'sks-dump-' + str(i).zfill(4) + '.pgp'

    if not os.path.exists(download_dir + '/' + file_name):
        print("Download " + file_name)
        wget.download(url + file_name, download_dir + '/' + file_name)

# import keys into temporary keyring
temp_keyring = 'temp_keyring.gpg'
temp_keyring_path = temp_dir_path + '/' + temp_keyring

for dump_file in os.scandir(download_dir):

    # import is going to finish with exit code != 0 because some of the keys might not be able to be imported, but that doesn't matter here.
    try:
        subprocess.call(['gpg', '--no-default-keyring', '--keyring', str(temp_keyring_path), '--fast-import',  dump_file.path])
    except subprocess.CalledProcessError:
        pass

# export ascii representations
gpg = gnupg.GPG(gnupghome=temp_dir, keyring=temp_keyring)
key_ids = [key['fingerprint'] for key in gpg.list_keys()] # raises exception (fingerprint collision) because library cannot handle revoked keys well

suffix = 0
for key_id in key_ids:
    with open(ascii_dir + '/' + str(suffix).zfill(10), 'w') as temp_ascii:
        temp_ascii.write(gpg.export_keys(key_id))

    suffix += 1

# insert keys into DHT
for ascii_file in os.scandir(ascii_dir):
    database.insert_key(ascii_file.path)
