import socket
import threading
from security.utility import encrypt, decrypt

host = '127.0.0.1'
port = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen()

connectedClients = []
usernames = []

def secure_send(client,data):
    token = encrypt(data)
    client.send(token)

def secure_recv(client,buffer_size):
    token = client.recv(1024)
    message = decrypt(token)
    return message

def broadcast(message): #function to send messages to everybody else
    for client in connectedClients:
        secure_send(client, message) #iterating through clients and sending the message

def handle_client(client): #catches and handles exceptions of each client computer, the client parameter is the person trying to send the message
    while True:
        try:
            message = secure_recv(client, 1024) #1024 is the maximum # of bytes a server can receive from a client
            broadcast(message) #if we made it this far, we want to display it to everybody else
        except:
            #in the case of errors and exceptions, we should identify the client that we need to remove and remove their username too
            index = connectedClients.index(client)
            connectedClients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has left the chat room.'.encode('utf-8')) #we have to write our messages like this because strings do not work
            usernames.remove(usernames)
            break

def receive(): #this is the primary function to receive client connections
    while True:
        print('Server is opened and now listening.')
        client, address = server_socket.accept() #the server.accept() method means it's waiting around constantly for any connections from any connection and it provides the address and connection of the client
        #once the line above catches something trying to connect, we should notify that a connection was established with somebody
        print(f'connection is established with {str(address)}')
        secure_send(client, 'What would you like your username to be?'.encode('utf-8')) #this message we send to that client in particular is like letting them know "hey, you're in! now what do you want to be called?"
        username = secure_recv(client, 1024) #whatever they send back will be saved
        usernames.append(username) #and then we add that new username into the list of usernames
        connectedClients.append(client)
        print(f'The username of the client is {username}'.encode('utf-8'))
        broadcast(f'{username} has connected to the chat room'.encode('utf-8'))
        secure_send(client, 'You are now connected.'.encode('utf-8'))

        #because the server needs to send and receive messages at the same time, we use multi-threading to make sure the other clients receive it instantaneously
        thread = threading.Thread(target = handle_client, args = (client,)) #the multiple threads take over this function here so that we can have multiple instances of the handle_client running at the same time
        thread.start()

if __name__ == "__main__":
    receive() #once the program starts, we run receive 