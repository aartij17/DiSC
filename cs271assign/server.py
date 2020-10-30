import socket
import os
import sys
import asyncio
import datetime
import queue
import hashlib
import random

if (len (sys.argv) < 2):
    print ("Usage: python3 server.py <pid>")
    sys.exit ()


class server:
    def __init__ (self, pid):
        self.pid = int(pid)
        self.set_config ("ipport-info.txt")


    def set_config(self, filename):
        f = open (filename, "r")
        # One thread for handling input
        send = f.readline().strip().split(" ")
        for i in range (self.pid):
            f.readline()
        recv = f.readline().strip().split(" ") # One thread for this

        f.close()

        self.send_host = send[0]
        self.send_port = int(send[1])
        self.recv_host = recv[0]
        self.recv_port = int(recv[1])

        self.ballot_num_accepted = 0
        self.no_quorum = {}
        self.my_ballot_num = 0
        self.prepare_quorum = []
        self.accept_quorum = []
        self.sent_accept = []
        self.accept_vals = {}
        self.request_queue = queue.Queue()
        self.ledger_filename = "ledger-" + str (self.pid) + ".txt"
        self.is_proposer = False
        self.phase_2 = False
        self.current_requests = []
        self.new_block = []

    def open_connection (self, loop):
        coro1 = asyncio.start_server(self.receive_data, self.recv_host, self.recv_port, loop=loop)
        server1 = loop.run_until_complete(coro1)

    async def find_nth(self, haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start


    async def receive_data (self, reader, writer):
        data = await reader.read(2048)
        await self.on_data_received (data)

    async def on_data_received (self, data):
        #lock = asyncio.Lock()
        data = data.decode("utf-8")
        print ("Data received: " + data)
        #print("\nReceived =  \t" + str(data)) 
        data_arr = data.split (" ")
        # data_arr[0] = Send to Process ID (1, 2, 3, 4, 5, 6), 6 is client
        # data_arr[1] = Send from Process ID (1, 2, 3, 4, 5, 6), 6 is client
        # data_arr[2] = Message Type, one of "moneyTransfer", "printBlockchain", "printBalance", "printSet", 
        #   "prepare", "ack", "accept", "acceptack1", "acceptack2", "decision", "request", "requestret"
        # data_arr[3] = depth
        # data_arr[4] = seq_num
        # data_arr[5:] = if Message Type = "decision",
        #               then is ledger information
        #async with lock:

        if int(data_arr[1]) > 5:
            await self.on_data_received_client (data)
        else:
            lock = asyncio.Lock()
            async with lock:
                await self.on_data_received_server ( data)

    async def on_data_received_client (self, data):
        print ("on_data_received_client")
        data_arr = data.split (" ")
        recv_from = int (data_arr[1])
        if (data_arr[2] == "moneyTransfer"):
            index = await self.find_nth (data, " ", 3)+1
            self.request_queue.put (data_arr[3:])
            await self.check_request_queue()
        lock = asyncio.Lock()
        async with lock:
            if (data_arr[2] == "printBlockchain"):
                await self.send_print_blockchain()
            elif (data_arr[2] == "printBalance"):
                await self.send_print_balance()
            elif (data_arr[2] == "printSet"):
                await self.send_print_set()


    async def read_blockchain (self):
        ledger = {}
        depth = 0
        with open (self.ledger_filename, "r+") as f:
            for line in f:
                arr = line.strip().split (" ")
                if len (arr) > 0:
                    ledger [int(arr[0])] = arr
                    depth = int(arr[0])+1

        return ledger, depth

    async def write_blockchain(self, new_ledger, depth):

        with open (self.ledger_filename, "w+") as f:
            for i in range (depth):
                new_line_arr = new_ledger [i]
                new_line = ""
                for substr in new_line_arr:
                    new_line += substr+ " "
                new_line = new_line[:-1] + "\n"
                f.write (new_line)

    async def calculate_balance (self):
        ledger, depth = await self.read_blockchain()
        money = [100, 100, 100, 100, 100]
        for i in range (depth):
            arr = ledger [i]
            sub_index = self.convert_ABC_to_index (arr[3])
            add_index = self.convert_ABC_to_index (arr[4])
            amount = float (arr[5])
            money [sub_index] -= amount
            money [add_index] += amount
            sub_index = self.convert_ABC_to_index (arr[6])
            add_index = self.convert_ABC_to_index (arr[7])
            amount = float (arr[8])
            money [sub_index] -= amount
            money [add_index] += amount
        return money


    async def send_print_blockchain (self):
        await self.send_update_ledger (5, 0)

    async def send_print_balance (self):
        money = await self.calculate_balance ()
        send_string = str (5) + " " + str (self.pid) + " printBalance "
        send_string += str (money[0]) + " " + str (money[1]) + " " + str (money[2]) + " " + str (money[3]) + " " + str (money[4]) 
        await self.send_message (send_string)

    async def send_print_set (self):
        ledger, depth = await self.read_blockchain()
        trans = []
        for i in range (depth):
            arr = ledger[i]
            trans.append ((arr[3], arr[4], arr[5]))
            trans.append ((arr[6], arr[7], arr[8]))
        
        send_string = str (5) + " " + str (self.pid) + " printSet "
        for tran in trans:
            send_string += tran[0] + " " + tran[1] + " " + tran[2] + ";"
        send_string = send_string[:-1]
        await self.send_message (send_string)


    async def on_data_received_server (self, data):
        data_arr = data.split (" ")
        recv_from = int (data_arr[1])
        if (data_arr[2] == "requestret"):
            index = await self.find_nth (data, " ", 3)+1
            await self.update_ledger(data[index:])
        elif (data_arr[2] == "request"):
            start = int (data_arr[3])
            await self.send_update_ledger(recv_from, start)
        else:
            newdepth = int(data_arr[3])
            ledger, depth = await self.read_blockchain()
            if depth < newdepth:
                self.ballot_num_accepted = 0
                await self.send_update_ledger_req (recv_from)
            elif depth == newdepth:
                await self.handle_paxos(data) 



    async def handle_paxos (self, data):
        data_arr = data.split(" ")
        recv_from = int (data_arr[1])
        #("prepare", "ack", "accept", "acceptack1", "acceptack2", "decision")

        msg_ballot_num = int (data_arr[4])
        depth = int(data_arr[3])

        if (data_arr[2] == "prepare"):
            if (self.ballot_num_accepted < msg_ballot_num):
                self.ballot_num_accepted = msg_ballot_num
                send_string = str(recv_from) + " " + str (self.pid) + " ack " + data_arr[3] + " " + data_arr[4]
                await self.send_message (send_string)
        elif (data_arr[2] == "ack"):
            if (self.ballot_num_accepted == msg_ballot_num):
                self.prepare_quorum.append (int (data_arr[1]))
                await self.check_prepare_quorum ()
        elif (data_arr[2] == "accept"):
            if (self.ballot_num_accepted == msg_ballot_num):
                send_string = str(recv_from) + " " + str (self.pid)
                if (depth in self.accept_vals):
                    ballot_num, data = self.accept_vals [depth]
                    if self.phase_2 and ballot_num < self.my_ballot_num and int(self.new_block[0]) == depth:
                        ballot_num = self.my_ballot_num
                        data = self.new_block

                    send_string += " acceptack2 " + str(depth) + " " + str(msg_ballot_num) + " " + str(ballot_num)
                    for val in data: 
                        send_string += " " + str(val)

                    self.accept_vals [depth] = (msg_ballot_num,  data_arr[5:])
                    await self.send_message (send_string)
                elif self.phase_2 and int(self.new_block[0]) == depth:
                    ballot_num = self.my_ballot_num
                    data = self.new_block

                    send_string += " acceptack2 " + str(depth) + " " + str(msg_ballot_num) + " " + str(ballot_num)
                    for val in data: 
                        send_string += " " + str(val)

                    self.accept_vals [depth] = (msg_ballot_num,  data_arr[5:])
                    await self.send_message (send_string)
                else:
                    self.accept_vals [depth] = (msg_ballot_num,  data_arr[5:])
                    send_string += " acceptack1 " + str (depth) + " " + str(msg_ballot_num)
                    await self.send_message (send_string)
        elif (data_arr[2] == "acceptack1" or data_arr[2] == "acceptack2"):
            if (self.ballot_num_accepted == msg_ballot_num):
                if (data_arr[2] == "acceptack2"):
                    if (depth in self.accept_vals):
                        if (self.accept_vals[depth][0] < int (data_arr[5])):
                            self.accept_vals[depth] = (int (data_arr[5]), data_arr[6:])
                    else:
                        self.accept_vals[depth] = (int (data_arr[5]), data_arr[6:])

                self.accept_quorum.append (int(data_arr[1]))
                await self.check_accept_quorum()
        elif (data_arr[2] == "decision"):
            self.ballot_num_accepted = 0
            index = await self.find_nth (data, " ", 5)+1
            block = data[index:].split (" ")

            if (int (block[0]) in self.no_quorum and self.no_quorum[int (block[0])] 
                and int (block[0]) == int(self.new_block[0])):
                self.no_quorum[int (block[0])] = False
                print (block)
                print (self.new_block)
                i = 0
                for val in block: 
                    if i < len (self.new_block):
                        if str (val) != str(self.new_block [i]):
                            self.no_quorum[int (block[0])] = True
                    else:
                        self.no_quorum[int (block[0])] = True
                    i+=1

                if (self.no_quorum[int (block[0])]):
                    print ("No Consensus reached")
                else:
                    print ("Consensus reached")

            await self.update_ledger(data[index:])



    async def update_ledger(self, data):
        ledger, depth = await self.read_blockchain ()
        blocks = data.split (";")
        for block in blocks:
            blk = block.split (" ")
            #print ("block=")
            #print (blk)
            cur_depth = int(blk[0])
            ledger[cur_depth] = blk
            if (cur_depth+1 > depth):
                depth = cur_depth+1

        await self.write_blockchain (ledger, depth)

    async def send_update_ledger (self, recv_from, start):
        ledger, depth = await self.read_blockchain ()
        send_string = str (recv_from) + " " + str (self.pid) + " requestret "
        for i in range (int(start), depth):
            block = ledger [i]
            for val in block:
                send_string += val + " "
            send_string = send_string [:-1] + ";"
        send_string = send_string [:-1]
        await self.send_message (send_string)

    async def send_update_ledger_req (self, recv_from):
        ledger, depth = await self.read_blockchain()
        send_string = str(recv_from) + " " + str(self.pid) + " request " + str(depth)
        await self.send_message (send_string)

    async def send_message (self, data):
        client_socket = socket.socket()  # instantiate
        client_socket.connect((self.send_host, self.send_port))  # connect to the server
        client_socket.send(data.encode())  # send message
        client_socket.close()  # close the connection
        print ("Data sent: " + data)

    async def validate_request (self, requests):
        money = await self.calculate_balance ()
        for request in requests:
            sub_index = self.convert_ABC_to_index (request[0])
            add_index = self.convert_ABC_to_index (request[1])
            amount = float (request[2])
            money [sub_index] -= amount
            money [add_index] += amount
            if (money[sub_index] < 0):
                return False
        return True

    async def check_request_queue (self):
        #print ("check_request_queue")
        lock = asyncio.Lock()
        cont = False
        async with lock:
            if self.request_queue.qsize() >= 2 and not self.is_proposer:
                self.is_proposer = True
                cont = True
                self.current_requests = []
                self.phase_2 = False
                while not self.request_queue.empty() and len (self.current_requests) < 2:
                    self.current_requests.append (self.request_queue.get())
                    flag = await self.validate_request (self.current_requests)
                    if not flag:
                        self.current_requests = self.current_requests[:-1]

        if (len (self.current_requests) >= 2 and cont):
            self.new_block = await self.obtain_new_block ()
            print ("new_block = ")
            print (self.new_block)
            await self.initiate_paxos(int(self.new_block[0]))

    async def obtain_new_block (self):
        lock = asyncio.Lock()
        async with lock:
            ledger, depth = await self.read_blockchain ()
        prev_sha = "NULL"
        if depth != 0:
            block = ledger[depth-1]
            #print ("Prev_block = ")
            #print (block)
            prev_sha = await self.calculate_sha256 (block)

        guess = 0
        new_block = [depth, prev_sha, guess, self.current_requests[0][0], self.current_requests[0][1], self.current_requests[0][2], 
                self.current_requests[1][0], self.current_requests[1][1], self.current_requests[1][2]]
        a = "8"
        while a[-1] != "0" and a[-1] != "1":
            guess +=1
            new_block = [depth, prev_sha, guess, self.current_requests[0][0], self.current_requests[0][1], self.current_requests[0][2], 
                self.current_requests[1][0], self.current_requests[1][1], self.current_requests[1][2]]
            a = await self.calculate_sha256 (new_block)
        #print ("new hash = ")
        #print (a)
        return new_block


    async def calculate_sha256 (self, block):
        m = hashlib.sha256()
        for val in block:
            m.update((str (val)).encode())
        return m.hexdigest ()

    async def initiate_paxos (self, depth):
        ledger, cur_depth = await self.read_blockchain ()
        self.no_quorum [depth] = True
        while (cur_depth == depth and self.no_quorum[depth]):
            lock = asyncio.Lock()
            async with lock:
                self.phase_2 = False
                self.prepare_quorum = []
                self.accept_quorum = []
                self.sent_accept = []
                self.my_ballot_num = 5 * int(1 + self.ballot_num_accepted / 5) + self.pid
                self.ballot_num_accepted = self.my_ballot_num
                for i in range (0, 5):
                    if (i != self.pid):
                        send_string = str (i) + " " + str (self.pid) + " prepare " + str(depth) +" " + str(self.my_ballot_num)
                        await self.send_message (send_string)
            await asyncio.sleep (20)
            if (self.no_quorum[depth]):
                ledger, cur_depth = await self.read_blockchain ()
                await asyncio.sleep (int(random.random()*60))

        if (self.no_quorum[depth]):
            self.request_queue.put (self.current_requests[0])
            self.request_queue.put (self.current_requests[1])
        self.ballot_num_accepted = 0
        self.my_ballot_num = 0
        self.prepare_quorum = []
        self.accept_quorum = []
        self.current_requests = []
        self.sent_accept = []
        self.is_proposer = False
        self.phase_2 = False
        #print ()
        #print ("RESET")
        await self.check_request_queue ()




    async def check_prepare_quorum (self):
        #print ('Before if')
        if (self.no_quorum[int (self.new_block[0])]): 
            #print ('After if')
            #print ("")
            #print ("self.prepare_quorum = " + str(self.prepare_quorum))
            #print ("self.is_proposer = " + str(self.is_proposer))
            #print ("self.phase_2 = " + str(self.phase_2))
            total = len (self.prepare_quorum)
            if (self.ballot_num_accepted == self.my_ballot_num):
                total += 1
            if (total >= 3):
                self.phase_2 = True
                for i in range (0, 5):
                    #print (i)
                    tmpb = ""
                    for val in self.sent_accept:
                        tmpb += str (val) + " "
                    #print ("tmpb = " + tmpb)
                    #print ("not i in self.sent_accept = " + str (not i in self.sent_accept))
                    #print ("i in self.prepare_quorum = " + str (i in self.prepare_quorum))
                    if (i != self.pid and not i in self.sent_accept and i in self.prepare_quorum):
                        self.sent_accept.append (i)
                        send_string = str (i) + " " + str (self.pid) + " accept " + str(self.new_block[0]) + " " + str(self.my_ballot_num)
                        #print (send_string)
                        for val in self.new_block:
                            send_string += " " + str(val)
                        await self.send_message (send_string)


    async def check_accept_quorum (self):
        if (self.no_quorum[int (self.new_block[0])]):   
            total = len (self.prepare_quorum)
            if (self.ballot_num_accepted == self.my_ballot_num):
                total += 1
            if (total >= 3):
                decision = self.new_block
                if (int (self.new_block[0]) in self.accept_vals):
                    #print ("Did not reach consensus")
                    decision = self.accept_vals[int (self.new_block[0])][1]
                else:
                    #print ("Reached consensus")
                    self.no_quorum[int (self.new_block[0])] = False

                data = ""
                for val in decision:
                    data += str(val) + " "
                data = data[:-1]
                #print ("Decision:")
                #print (data)
                for i in range (0, 5):
                    if (i != self.pid):
                        send_string = str (i) + " " + str (self.pid) + " decision " + str(self.new_block[0]) + " " + str(self.my_ballot_num) + " " + data
                        await self.send_message (send_string)
                    else:
                        await self.update_ledger(data)


    def convert_ABC_to_index (self, val):
        if (val == "A"):
            return 0
        elif (val == "B"):
            return 1
        elif (val == "C"):
            return 2
        elif (val == "D"):
            return 3
        else:
            return 4 



if __name__ == '__main__':
    server1 = server(sys.argv[1])
    loop = asyncio.get_event_loop()
    server1.open_connection(loop)
    loop.run_forever()
