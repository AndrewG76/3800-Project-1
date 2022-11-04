from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

PASSWORD = "mypassword"

# def hasKeyOnFile(user: str):
#     return exists(f"{cwd}/keys/{user}.pem")


def getHash(section):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(section.encode())
    hash = digest.finalize()
    return hash

def encrypt(message, key):
    if not type(message) == bytes:
        message.encode()
    ciphertext = key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt(message, my_priv_key):
    plaintext = my_priv_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def genKey():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key



def sign(message, priv_key):
    signature = priv_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify(signature, message, pub_key):
    pub_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# _saveKey(f"{cwd}/keys/server_keys/2022-10-26.pem", _genKey())

# def registerNewUserKeys(user):
#     private_key = _genKey()
#     _saveUserKey(user, private_key)

# ###
# def _saveUserKey(user, key, isPriv=True):
#     _saveKey(f"{cwd}/keys/user_keys/{user}.pem", key, isPriv)

# def _loadUserKey(user, isPriv):
#     return _loadKey(f"{cwd}/keys/user_keys/{user}.pem", isPriv)

# def _saveServerKey(date, isForSig, key, isPriv=True):
#     purpose = "sig" if isForSig else "enc"
#     _saveKey(f"{cwd}/keys/server_keys/{date}_{purpose}.pem", key, isPriv)

# def _loadServerKey(date, isForSig, isPriv=True):
#     purpose = "sig" if isForSig else "enc"
#     return _loadKey(f"{cwd}/keys/server_keys/{date}_{purpose}.pem", isPriv)
###
