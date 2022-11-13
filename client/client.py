import threading
import socket

from security import utility
from security.utility import encrypt, decrypt, serializePubKey
import security

SEP = b"|||"
BUFFER_SIZE = 4096
username = input('Please input a username: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1234))

def secure_send(data):
    token = encrypt(data)
    client.send(token)

def secure_recv(buffer_size):
    token = client.recv(BUFFER_SIZE)
    message = decrypt(token)
    return message

rsa_key = utility.genKey()
#we want a function for receiving messages from other clients
def client_receive():
    try:
        while True:
            decrypt_successful = False
            message = client.recv(BUFFER_SIZE)
            if message.split(SEP)[0] == b"AES_ENCRYPTED":
                message = decrypt(message.split(SEP)[1])
                decrypt_successful = True
            else:
                message = message.split(SEP, 1)[1]
            if message == b"INITIALIZE_SECURITY": # the first message sent by the server to initialize a security
                client.send(serializePubKey(rsa_key.public_key()))
            elif message.split(SEP)[0] == b"KEY": 
                c = message.split(SEP)[1]
                aesKey = utility.rsaDecrypt(c,rsa_key)
                utility.saveAESKey(aesKey)
            elif decrypt_successful and message == b"GET_USERNAME": #after we get this phrase here from the server, it then sends on over the username we made earlier from the top of the program
                secure_send(username.encode('utf-8'))
            elif decrypt_successful:
                print(message.decode('utf-8')) #because this message is not being sent to the server anymore, we have the ability to still use our terminal
    except Exception as e:
        print('Error encountered in client_receive thread') #generic in case something weird happens
        print(e)
        client.close() #we close our client if something weird happens and then this information gets relayed on over to the other clients via the server's emessages
        

def client_send():
    try:
        while True:
            message = f'{username}: {input("")}' #what this does is spit out into the messages that "[your username]" and then the message you want to say after kinda like a chat in like Twitch for example
            secure_send(message.encode('utf-8')) #and now we relay our message on over to the server which then spits out our message to the other clients connected
    except:
        print('Error encountered in client_send thread')
        client.close()

receive_thread = threading.Thread(target = client_receive)
receive_thread.start()

send_thread = threading.Thread(target = client_send)
send_thread.start()


#and we want a function for sending messages to other clients