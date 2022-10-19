#server.py
import socket
 
# socket server
ip = ''  
port = 8888
socket_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# 2.ip,port
socket_server.bind((ip, port))
# 3.start listening
socket_server.listen(1)  # block when more than one connection, allowed only one connection
while True:
    conn, addr = socket_server.accept()  # wait untill there is new connection
    with conn:
        print("connect by", addr)
        try:
            while True:
                data = conn.recv(1024)
                print("server recevie peername and data:", conn.getpeername(), data.decode())
                if data:
                    # conn.sendall(data)  # retutrn all data to client
                    response = input(">>>")
                    conn.sendall(response.encode())
                    print("send to client:", response)
                else:
                    break
        except ConnectionResetError as e:
            print("Disconnected ")
#asdfasdlkfj;lasdhjfl;asjdlf