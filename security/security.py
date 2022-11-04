import enc_interface as ei
from cryptography.hazmat.primitives import serialization
def verifyIntegrity(user, content, sig):
    pass


private_key = ei.genKey()
pem = private_key.private_bytes(

   encoding=serialization.Encoding.PEM,

   format=serialization.PrivateFormat.PKCS8,

   encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')

)
print(type(pem))
print(ei.sign(pem, ei.genKey()))
# print(ei.encrypt(pem, ei.genKey().public_key()))
