from cryptography.fernet import Fernet
import os


def loadKey():
    cwd = "security/" if \
        os.path.exists("security") else ""
    key = None
    with open(cwd + "key", "rb") as file:
        key = file.read()
    return key

def encrypt(message):
    key = loadKey()
    f = Fernet(key)
    token = f.encrypt(message)
    return token

def decrypt(token):
    key = loadKey()
    f = Fernet(key)
    message = f.decrypt(token)
    return message

# message = b"Hello friends! Respond if you got my message please"

# token = encrypt(message)
# message = decrypt(token)
# print(token)
# print(message)
