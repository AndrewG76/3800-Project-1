from cryptography.fernet import Fernet
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def genKey():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key

def serializePubKey(key):
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem

def deserializePubKey(pem):
    key = serialization.load_pem_public_key(
                pem
            )
    return key


def saveAESKey(key):
    cwd = "client/security/" if \
        os.path.exists("client/security/") else ""         ""
    with open("key", "wb") as file:
        file.write(key)
    return key

def loadAESKey():
    cwd = "client/security/" if \
        os.path.exists("client/security/") else ""
    key = None
    with open(cwd + "key", "rb") as file:
        key = file.read()
    return key

def encrypt(message):
    key = loadAESKey()
    f = Fernet(key)
    token = f.encrypt(message)
    return token

def decrypt(token):
    key = loadAESKey()
    f = Fernet(key)
    message = f.decrypt(token)
    return message

def rsaEncrypt(message, key):
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

def rsaDecrypt(message, my_priv_key):
    plaintext = my_priv_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


# message = b"Hello friends! Respond if you got my message please"

# token = encrypt(message)
# message = decrypt(token)
# print(token)
# print(message)
