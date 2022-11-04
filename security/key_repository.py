from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey
PASSWORD = b"password123"


def loadKey(path, isPriv=True):
    with open(path, "rb") as key_file:
        if isPriv:
            key = serialization.load_pem_private_key(
                key_file.read(),
                password=PASSWORD
            )
        else:
            key = serialization.load_pem_public_key(
                key_file.read()
            )
    return key

def saveKey(path, key):
    isPriv = True if type(key) == _RSAPrivateKey else False
    if isPriv:
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(PASSWORD)
        )
    else:
        pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path,mode="wb") as file:
        file.write(pem)