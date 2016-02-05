import gnupg


def get_address(key_file):
    gpg = gnupg.GPG(gnupghome='./temp')
    key = gpg.scan_keys(key_file)

    addresses = []

    for uid in key[0]['uids']:
        addresses.append(uid.split('<')[1].split('>')[0])

    return addresses


def get_id(key_file):
    gpg = gnupg.GPG(gnupghome='./temp')
    key = gpg.scan_keys(key_file)

    if len(key) < 1:
        return -1

    key_id_string = key[0]['keyid']
    key_id = key_id_string[-8:]

    return key_id


def get_info(key_file):
    gpg = gnupg.GPG(gnupghome='./temp')
    key = gpg.scan_keys(key_file)

    return key
