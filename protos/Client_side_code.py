import socket
import time

# create a socket based on tcp/ip protocol
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# creation of udp/ip protocol
# udpSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#IP/ IP/port number
host = "localhost"
port = 8888
Address = (host, port)

# start connecting to the server
clientSocket.connect(Address)

if clientSocket is None:
    print("Sorry,can not connected to the server.....NO")

else:
    print("Successful, connected to the server-----OK")
    while True:
        Client_data = input("My[client]=====>Please enter message send to server(exit/quit)  :")
        #time.sleep(0.5)
        if Client_data.lower() =="exit" or Client_data.lower() =="quit":
            #bytes 
            clientSocket.send(bytes("EXIT".encode("UTF-8")))
            # close current client connction
            print("Disconnected...")
            clientSocket.close()
            break

        clientSocket.send(bytes(Client_data.encode("UTF-8")))

        #Receiveing data/message from server
        Client_data_finally = clientSocket.recv(1024).decode("UTF-8")
        print("[Sys response] message from server:%s"%Client_data_finally)

        #print("message from client:{0}".format(str(data_finally)))



