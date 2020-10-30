import socket
import random
import time
import threading
from _thread import *
min_delay = 0.1
max_delay = 4.1

f2 = open ("nwprocess-config.txt", "r")
min_delay = float(f2.readline())
max_delay = float(f2.readline())
f2.close()

class nwprocess: 
    
    def __init__ (self, filename):
        #self.q = asyncio.Queue()
        self.set_config(filename)

    def set_config (self, filename):
        f = open (filename, "r")
        # One thread for handling input
        #recv = f.readline().strip().split(" ")
        
        #self.host = recv[0]
        #self.port = int (recv[1])
        #self.host = "127.111.43.21"
        self.host = "localhost"
        self.port = 4000

        self.send_to = []
        for i in range (4):
            self.send_to.append(f.readline().strip().split(" "))

        f.close()


    def start_nwprocess (self):
        global min_delay
        global max_delay
        
        s = socket.socket ()
        s.bind ((self.host, self.port))
        print ("nwprocess opened on host " + str (self.host) + " port " + str (self.port))
        print ("min delay = ", min_delay)
        print ("max delay = ", max_delay)

        s.listen (5)
        while (True):
            conn, addr = s.accept()
            start_new_thread (self.receive_data, (conn,))
        
    def receive_data(self, reader):
        data = reader.recv(1024)
        data = data.decode ("utf-8")

        rand = random.uniform(min_delay, max_delay)
        time.sleep(rand)
        parse = data.split (" ")
        print (str(parse[2:]) +"\tfrom server " +str (parse[1])+ "->" + str(parse[0])+ " (delay " + str (rand)+ " seconds)")
        receiver = int (parse[0])

        client_socket = socket.socket()  # instantiate
        #print (self.send_to[receiver][0])
        #print (self.send_to[receiver][1])
        client_socket.connect((self.send_to[receiver][0], int(self.send_to[receiver][1])))  # connect to the server
        client_socket.send(data.encode()) # send message
        client_socket.close()  # close the connection


def server_program ():
    p1 = nwprocess ("ipport-info.txt") 
    p1.start_nwprocess()


if __name__ == '__main__':
    server_program()
