import time
import key_repository
import enc_interface as ei

SEP = b"|||||"
SEP2 = b"-----"
SEP3 = b"+++++"
cwd = "security"

def serialize(message):
    return str(message).encode()

def stamp(message):
    return serialize(time.time()) + SEP2 + message

def unstamp(message):
    return message.split(SEP2)

def encrypt(message, puKey):
    return ei.encrypt(message, puKey)

def decrypt(message, prKey):
    return ei.decrypt(message, prKey)
    
def unparse(message):
    action, params = message.split(SEP)
    return action, params

def sign(message, prKey):
    sig = ei.sign(message, prKey)
    return sig + SEP3 + message

def verifySig(sig, message, puKey):
    ei.verify(sig, message, puKey) #will raise exception if verification fails

def sepSig(message):
    sig, message = message.split(SEP3)
    return sig, message

def pack(message, theirEKey, mySKey):
    message = stamp(message)
    message = encrypt(message, theirEKey)
    message = sign(message, mySKey)
    return message

def unpack(package, theirVKey, myDKey, isEnc=True):
    sig, package = sepSig(package)
    signed_content = package
    package = decrypt(package, myDKey)
    timestamp, message = unstamp(package)
    action, params = unparse(message)
    verifySig(sig, signed_content,theirVKey)
    return timestamp, action, params 

#############################################################
# Enough with the function definitions! Show what it looks like to use them!

#server's public key   (clients encrypt with this key to)
sPuKey = key_repository.loadKey(cwd + "/keys/sPuKey.pem", False)  

#server's private key  (only the server has this key, so only the server can decrypt what has been decrypted)
sPrKey = key_repository.loadKey(cwd + "/keys/sPrKey.pem", True)

#similar, but for the client
cPuKey = key_repository.loadKey(cwd + "/keys/cPuKey.pem", False)   #client's public key
cPrKey = key_repository.loadKey(cwd + "/keys/cPrKey.pem", True)    #client's private key

# example message to be sent to server
# it has the format "ACTION + SEPARATOR + PARAMETERS"
message = b"COMMENT" + SEP + b"Hello world!"

# The client prepares the message before sending it the server.
# Get an encrypted form of the message so only the server can read it
# and pack some other useful information like time sent
super_secure_package = pack(message,sPuKey,cPrKey)

print("="*30 + "\nMost of the package is encrypted and looks like gibberish.")
print("The package looks like this:\n\n" + str(super_secure_package)) #print the result

# The server will call this function when it receives the
# super_secure_package over the internet.
# It just extracts the contents and decrypts the message so
# the server can read what it says.
timestamp, action, params = unpack(super_secure_package, cPuKey, sPrKey)

print("="*30 + " \n Heres what the server extracts from the package after receiving it: \n") #print the result
print(f"timestamp: {str(timestamp)}\naction: {str(action)}\nparams: {str(params)}\n\n")
print("The timestamp does not consist of a time and date.")
print("Instead it is in seconds since the epoch.\nThe epoch is January 1 of 1970.")
print("It gives a convenient way to store time without having to parse which parts are the seconds, minutes, day, and other fields")



