import datetime
import rsa


class PGPEntry(object):
    def __init__(self, email, pub, date):
        self.email = email
        self.pub = pub
        self.date = date
        self.sig = []

    def __str__(self):
        return self.email

    # sign key instance by <signer_email> with secret key <signer_sec>
    def sign(self, signer_email, signer_sec):
        sig = rsa.sign(str(self.email) + ', ' + str(signer_email) + ', ' + str(datetime.date.today()), signer_sec, 'SHA-256')
        self.sig.append(Signature(self.email, signer_email, datetime.date.today(), sig))


class PGPKey(object):
    def __init__(self, email):
        self.email = email

        # generate new key pair
        (pubkey, privkey) = rsa.newkeys(512)

        self.sec = str(privkey)
        self.pgp_entry = PGPEntry(self.email, str(pubkey), datetime.date.today())


class Signature(object):
    # <signee_email> is signed by <signer_email> on <date>. <sig> is signed string "<signee_email>, <signer_email>, <date>"
    def __init__(self, signee_email, signer_email, date, sig):
        self.signee_email = signee_email
        self.signer_email = signer_email
        self.date = date
        self.sig = sig

    def __str__(self):
        return "Signee: " + str(self.signee_email) + ", Signer: " + str(self.signer_email) + ", Date: " + str(self.date) + "Sign: " + str(self)
