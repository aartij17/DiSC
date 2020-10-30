import socket
import datetime

send_host = "128.111.43.21"
send_host = "localhost"
send_port = 4000
pid = 0

def send_message (send_string):
    host = send_host
    port = send_port
    #print ("Sending message")
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_socket.send(send_string.encode())  # send message
    client_socket.close()  # close the connection
    #print ("Sent message")

def server_program():
    # get the hostname
    host = socket.gethostname() 
    port = 5000  # initiate port no above 1024

    f = open ("ipport-info.txt", "r")
    server_addr = f.readline().split(" ");
    f.close();
    host = server_addr[0]
    port = int (server_addr[1]);

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    
    print ("Server started on host=", host, " port=", port)

    # configure how many client the server can listen simultaneously

    while True:

        server_socket.listen(4)
        conn, address = server_socket.accept()  # accept new connection
        print()
        print("Connection from:       \t " + str(address))
        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        print("from connected user:   \t " + str(data))
        user = data.split(" ")[1]

        time = datetime.datetime.now()
        data = user + " " + str(pid) + " " + time.strftime ("%Y/%m/%d/%H/%M/%S/%f")
        print ("Time Sent (Tutc) =    \t", time.strftime ("%m/%d %H:%M:%S.%f"))
        send_message(data) 

        #conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection



if __name__ == '__main__':
    server_program()
