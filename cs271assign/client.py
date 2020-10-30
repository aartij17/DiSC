import socket
import datetime
import time
import os
import signal
import sys
import threading
from _thread import *
import csv

if (len (sys.argv) < 2):
    print ("Usage: python3 client.py <pid> <config filename>")
    sys.exit ()

verbose = (len(sys.argv) > 2 and sys.argv[2] == "-v")


tau = 5
delta = 10
rho = 0.5
sleep_time = delta / (2 * rho)

pid = int(sys.argv[1])

f = open (sys.argv [2], "r")
delta = float (f.readline())
rho = float (f.readline())
f.close()

last_updated = datetime.datetime.now()
sim_time = datetime.datetime.now()
timer = datetime.datetime.now()

lock = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()
verbose = False


#recv_host = "128.111.43.21"
recv_host = "localhost"
recv_port = 5001

#send_host = "128.111.43.21"
send_host = "localhost"
send_port = 4000

num_nodes = 3
buffer_ledger = []
ledger_file = "ledger" + str(pid)
current_balance = []
saved_time = datetime.datetime.now()
saved_balance = []

def initialize_ledger ():
    global buffer_ledger
    global current_balance
    global saved_balance
    for i in range (num_nodes):
        buffer_ledger.append (["initial", -1, i+1, 10])
        current_balance.append (10)
    saved_balance = current_balance.copy()
    open(ledger_file, "w").close() 
    commit_to_ledger (buffer_ledger)
    buffer_ledger = []

def commit_to_ledger (buffer_ledger):
    global lock3
    lock3.acquire()
    with open(ledger_file, "a") as f:
        csvwriter = csv.writer (f, delimiter=',')
        for line in buffer_ledger:
            csvwriter.writerow (line)
    
    lock3.release()

def config(filename):
    global recv_host
    global recv_port
    f = open (filename, "r")
    # One thread for handling input
    #recv = f.readline().strip().split(" ")
    #host = recv[0]
    #port = int (recv[1])
    send_to = []
    for i in range (4):
        send_to.append(f.readline().strip().split(" "))
    f.close()
    
    recv_host = send_to[pid][0]
    recv_port = int(send_to[pid][1])


def server():
    s = socket.socket ()
    s.bind ((recv_host, recv_port))
    print ()
    print ("Started listening on host " + recv_host + " port " + str (recv_port))
    s.listen (3)
    while (True):
        conn, addr = s.accept()
        start_new_thread (receive_server, (conn,))


def receive_server (reader):
    data = reader.recv (1024)
    data = data.decode ("utf-8")
    print ()
    print ("Received data -> " + data)
    data_arr = data.split (" ")
    if (data_arr[1] == "0"):
        new_time_handler(data_arr[2])
    else:
        consensus_handler(data)
    
def send_message (send_string):
    host = send_host
    port = send_port
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_socket.send(send_string.encode())  # send message
    client_socket.close()  # close the connection  


def printTimeHandler():
    global lock
    lock.acquire()
    now = datetime.datetime.now()
    curr = calculate_time (sim_time, now-last_updated,rho)
    print ()
    print ("Simulated Time: \t\t", curr.strftime ("%m/%d %H:%M:%S.%f"))
    print ("Actual Time:    \t\t", now.strftime ("%m/%d %H:%M:%S.%f"))
    print ("Time delta:     \t\t", curr - now)
    lock.release()


def consensus_handler(data):
    global buffer_ledger
    global current_balance
    #global saved_time
    #global saved_balance
    global lock2
    
    data_split = data.split(" ")

    lock2.acquire()
    transtime = data_split[2]
    send_from_pid = int (data_split[3])
    send_to_pid = int(data_split[4])
    send_amt = int (data_split[5])
    buffer_ledger.append([transtime, send_from_pid, send_to_pid, send_amt])
    current_balance[send_to_pid-1] += send_amt
    current_balance[send_from_pid-1] -= send_amt

    """
    trans_time = datetime.datetime.strptime(transtime, "%Y/%m/%d/%H/%M/%S/%f") 
    if (trans_time < saved_time):
        current_balance[send_to_pid] += send_amt
        current_balance[send_from_pid] -= send_amt
    """

    lock2.release()


def user_input (no_args):
    while (True):
        print ("Enter action ")
        print ("  (1) - enter transaction ")
        print ("  (2) - balance transaction")
        print ("  (3) - print time")

        line = input("-> ")
        line = line.strip()

        if (line == "1"):
            line2 = input("Enter Transaction: ")
            line2 = line2.strip()
            line_arr = line2.split(" ")
            #if (len(line_arr) == 3):
            #if (line_arr[0] == str(pid) and (line_arr[1] == "1" or line_arr[1] == "2" or line_arr[1] == "3") and line_arr[2] != str(pid)):        
            start_new_thread (request, (line2,))
        elif (line == "2"):
            start_new_thread (balanceTransaction, ("",))
        elif (line == "3"):
            printTimeHandler()



def request (req):
    global current_balance
    global buffer_ledger
    global lock2

    now = datetime.datetime.now()
    curr_time =  calculate_time (sim_time, now-last_updated,rho)
    current_time =  curr_time.strftime ("%Y/%m/%d/%H/%M/%S/%f") 
    
    request = req.split(" ")
    if (len(request) != 3):
        print ("Usage: <ThisPID> <ReceivePID> <Amount>")
    elif (not (request[0].isdigit() and request[1].isdigit() and request[2].isdigit())):
        print ("Usage: <ThisPID> <ReceivePID> <Amount>")
    elif (int(request[1]) > num_nodes):
        print ("Invalid PID")
    elif (int(request[0]) != pid):
        print ("Incorrect PID")
    elif (int(request[2]) > current_balance[pid-1]):
        print ("Not enough money for transaction")
    else:
        lock2.acquire()
        current_balance[int(request[1])-1] += int(request[2])
        current_balance[int(request[0])-1] -= int(request[2])
        buffer_ledger.append ([current_time, int(request[0]), int(request[1]), int(request[2])])
        lock2.release()
        for i in range (num_nodes):
            if (i+1 != pid):
                send_str = str (i+1) + " " + str (pid) + " " + current_time + " " + req
                send_message (send_str)
        
        time.sleep (delta + tau)
        sort_ledger()
        lock2.acquire()
        while (len(buffer_ledger) > 0 and datetime.datetime.strptime(buffer_ledger[0][0], "%Y/%m/%d/%H/%M/%S/%f") <= curr_time):
            commit_to_ledger ([buffer_ledger.pop(0)])
        lock2.release()
        print ("SUCCESS")
        evaluateBalance(curr_time)

def balanceTransaction(noargs):
    now = datetime.datetime.now()
    curr_time = calculate_time (sim_time, now-last_updated,rho)
    time.sleep(delta+tau)
    sort_ledger()

    lock2.acquire()
    while (len(buffer_ledger) > 0 and datetime.datetime.strptime(buffer_ledger[0][0], "%Y/%m/%d/%H/%M/%S/%f") <= curr_time):
        commit_to_ledger ([buffer_ledger.pop(0)])
    
    evaluateBalance (curr_time)
    lock2.release()

def evaluateBalance(curr_time):

    global lock3
    lock3.acquire()
    balance = 0
    with open(ledger_file, "r") as f:
        csvreader = csv.reader (f, delimiter=',')
        for line in csvreader:
            if (line [0] == "initial" or datetime.datetime.strptime(line[0], "%Y/%m/%d/%H/%M/%S/%f") <= curr_time):
                if int(line[1]) == pid : 
                    balance -= int(line[3])
                elif int(line[2]) == pid:
                    balance += int(line[3])
    lock3.release()
    print ()
    print ("Your balance of process " + str(pid) +  " is $" + str(balance) + " as of " + curr_time.strftime ("%m/%d %H:%M:%S.%f"))


def sort_ledger():
    lock2.acquire()
    global buffer_ledger
    buffer_ledger = sorted(buffer_ledger, key=lambda x: x[0])
    lock2.release()

def simulation (): 
    global delta 
    global rho 
    global sleep_time
    sleep_time = delta / (2 * rho)
    print ("ProcessID = "+str(os.getpid()))
    print ("delta     = "+str(delta))
    print ("rho       = "+str(rho))
    print ("sleep_time= "+str(sleep_time))
    config("ipport-info.txt")
    initialize_ledger()
    start_new_thread(clock, ("",))
    start_new_thread(user_input, ("",))
    server()

def clock(no_args):
    global last_updated
    global sim_time
    sim_time = datetime.datetime.now()
    global timer
    timer = datetime.datetime.now()
    global first_time
    first_time = True
    
    while (True):
        if (verbose):
            print ()
            print ("---- Querying Time Server ----")

        if(not first_time and verbose):
            now = datetime.datetime.now()
            T1 = calculate_time (sim_time, now-last_updated,rho)
            print ("T1 =                         \t", T1.strftime ("%m/%d %H:%M:%S.%f"))
        
        timer = datetime.datetime.now()
        query_server()
        
        time.sleep (sleep_time)


def new_time_handler(from_server):
    global lock
    lock.acquire()
    global first_time
    global timer
    global sim_time
    global last_updated
    new_time = datetime.datetime.strptime(from_server, "%Y/%m/%d/%H/%M/%S/%f") 

    if(not first_time and verbose):
        now = datetime.datetime.now()
        T2 = calculate_time (sim_time, now-last_updated,rho)
        print ("T2 =                         \t", T2.strftime ("%m/%d %H:%M:%S.%f"))
 

    print ("Received From Server (Tutc) =  \t", new_time.strftime ("%m/%d %H:%M:%S.%f"))

    timedelta = datetime.datetime.now() - timer
    timedelta = timedelta/2
    sim_time = new_time + timedelta
    last_updated = sim_time
    print ("Set time to (T') =           \t", sim_time.strftime ("%m/%d %H:%M:%S.%f"))
    first_time = False
    lock.release()
        

def query_server():
    message = "0 " + str(pid) + " QueryTime"  # take input
    send_message (message)


def calculate_time (sim_time_at_sync, timedelta, rho):
    return sim_time_at_sync + (timedelta) * (1+rho)
    

if __name__ == '__main__':
    simulation()
