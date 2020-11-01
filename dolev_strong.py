
# class Protocol:
#     def connect(self) -> bool:  

#     def run(self) -> bool:
#     
# 
#       We want the ability to pass any consensus decision back up to the node that is running the protocol.
#       The node can run the protocol in a separate process with the multiprocessing library. The procol can wrote the decision to a 
#       pipe and the node can be waiting for it.
import json
import threading
import socket

class DolevStrong:

    class Message:
        def __init__(self, r):
            self.round = r
            self.signatures = set()

        def add_signature(self, sig):   
            # Check if sig not in self.signatures
            if sig not in self.signatures:
                self.signatures.add(sig)

        def create_message(self):
            return str(self.round) + "|" +  json.dumps(self.signatures)


    def listener(self, ip, port, f):
        decision = 0
        sock = socket.socket(socket.AF_INET, socket.sock_DGRAM)
        sock.bind((ip, port))
        while True:
            data, addr = sock.recvfrom(1024)  # I am not sure what to put here for a message limit
            messagecomponents = data.split("|")
            if messagecomponents[0] == "0":
                decision = 0

                # If this message is a b0 message, then this is the first round of Dolev-Strong
                for i in range(1, f + 2):
                    if decision == 0:
                        print("STUB")
                        # Wait to receive a message. Check the signatures. Then add your own signature to the end and broadcast
                    else:
                        break
                
                # Decision is made. Pass the decision to somewhere

    def start_protocol(self):
        while True:
            # Wait on some form of user input to initiate the protocol (probably from the pipe)


            # Send b0 to every node
            b0 = self.Message(0)
            # TODO: Send b0.create_message() to everyone

    def run(self, params) -> bool:
        # Setup pipe connection

        threading.Thread(target=self.listener, args=(params["ip"], params["port"], params["f"],)).start()
        threading.Thread(target=self.start_protocol).start()


