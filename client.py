import threading
import socket

from security.utility import encrypt, decrypt

username = input('Please input a username: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1234))

def secure_send(data):
    token = encrypt(data)
    client.send(token)

def secure_recv(buffer_size):
    token = client.recv(1024)
    message = decrypt(token)
    return message

#we want a function for receiving messages from other clients
def client_receive():
    try:
        while True:
            message = secure_recv(1024).decode('utf-8') #we are decoding here because now we are reciving the juicy message in this function
            if message == "What would you like your username to be?": #after we get this phrase here from the server, it then sends on over the username we made earlier from the top of the program
                secure_send(username.encode('utf-8'))
            else:
                print(message) #because this message is not being sent to the server anymore, we have the ability to still use our terminal
    except:
        print('Error encountered') #generic in case something weird happens
        client.close() #we close our client if something weird happens and then this information gets relayed on over to the other clients via the server's emessages
        

def client_send():
    while True:
        message = f'{username}: {input("")}' #what this does is spit out into the messages that "[your username]" and then the message you want to say after kinda like a chat in like Twitch for example
        secure_send(message.encode('utf-8')) #and now we relay our message on over to the server which then spits out our message to the other clients connected

receive_thread = threading.Thread(target = client_receive)
receive_thread.start()

send_thread = threading.Thread(target = client_send)
send_thread.start()


#and we want a function for sending messages to other clients