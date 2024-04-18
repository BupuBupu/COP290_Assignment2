import socket
from _thread import *
import sys

server = "10.184.5.134/19"
port = 5555 # 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) # we will bind whatever ip address we will get to this given port 
except socket.error as e:
    str(e)

s.listen(3) # for no. of connections, i.e. no. of people to connect
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    # continuously run while the client is connected
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048) # amount of information trying to receive, just inc. this size if getting error, larger the size, larger the time to receive info
            reply = data.decode("utf-8") # we are receiving encoded info
            
            if not data:
                print("Disconneccted")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            
            conn.sendall(str.encode(reply)) # encode and send the info
        except:
            break
    print("Lost connection")
    conn.close()

while True: # continuously look for connections
    conn, addr = s.accept() # accept any incoming connections, conn is connection object connected, addr is ip address
    print("connected to:", addr)
    
    start_new_thread(threaded_client, (conn,)) # this means that it gonna continue running without making this function finish, so it will act as background process, so threaded_client will run in background