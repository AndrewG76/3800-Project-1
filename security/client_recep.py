import time
import key_repository as kr
import enc_interface as ei
SEP = b"|||||"

def serialize(message):
    return str(message).encode()

def stamp(message):
    return serialize(time.time()) + SEP + message

def unstamp(message):
    return message.split(SEP)

def encrypt(message, puKey):
    return ei.encrypt(message, puKey)

def decrypt(message, prKey):
    return ei.decrypt(message, prKey)
    
def unparse(message):
    action, params

# message is action&content
def pack(message, theirEKey, mySKey):
    message = stamp(message)
    message = encrypt(message, theirEKey)
    message = sign(message, mySKey)
    return message

def unpack(message, theirVKey, myDKey):
    content = decrypt(message, myDKey)
    timestamp, message = unstamp(content)
    action, params = unparse(message)
    verify(content,theirVKey)
    return timestamp, message

cPrKey = kr.loadKey("keys/cPrKey.pem", True)
cPuKey = kr.loadKey("keys/cPuKey.pem", False)
sPrKey = kr.loadKey("keys/sPrKey.pem", True)
sPuKey = kr.loadKey("keys/sPuKey.pem", False)

print(unpack(pack(b"Hello there!", sPuKey, cPrKey), cPuKey, sPrKey))


