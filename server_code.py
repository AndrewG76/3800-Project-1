import socket
import time

# create a socket based on the tcp protocal
tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


# udpSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#IP/port Number
host = "localhost"
port = 8888
Address = (host,port)

# bond to the address
tcpSocket.bind(Address)
tcpSocket.listen(5)

while True:
    print("-"*15,"Server waiting to be connected","-"*15)
    client_sock,client_add = tcpSocket.accept()
    print("connected to the server，IP：{0}".format(client_add))
    try:
        print("*"*20," waiting for receiving data","*"*20)
        while True:
            #receiving datas from clien to server 
            Client_databack = client_sock.recv(1024)
            print("Message sent from client：{0}".format(str(Client_databack,encoding="UTF-8")))

            if Client_databack.upper() == "EXIT":
                break

            # # Date and time set for 24h mode when gethering time from PC    %I：12hHour mode   %H：24 hour mode
            Now_time = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())

            # Data respense from server to client
            #client_sock.send(bytes(data.encode("UTF-8")))
            client_sock.send(bytes("time = {0}，data = {1}".format(Now_time, str(Client_databack, encoding="UTF-8")), encoding="UTF-8"))

            Server_data = input("My[Server]=====>Please enter the message(s) that will send to client  ：")
            client_sock.send(Server_data.encode("UTF-8"))

            #接收客户端向服务器发送的数据
            Server_databack = client_sock.recv(1024).decode("UTF-8")
            print("Message received from client：%s" % Server_databack)

    except Exception as abc:
        print(abc)

    finally:
        client_sock.close()


