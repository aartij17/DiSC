class Node:
    def __init__(self, node_id, protocol, np, adversary=False):
        self.id = node_id
        self.received_messages = []
        self.committed_log = []
        self.protocol = protocol
        self.np = np
        self.adversary = adversary
        self.signatures = set()
        
    def get_id(self):
        return self.id

    def run_protocol_one_round(self):
        # store messages in local memory
        self.received_messages = []

        # received_messages is a list of messages which this node i received
        # these messages are processed by the protocol
        self.received_messages = self.np.receive_messages(self.get_id())
        print("received messages: ", self.received_messages)
        # run protocol with stored messages
        send_messages = self.protocol.run(self.received_messages, self.get_id(), self.committed_log)
        print("send messages: ", send_messages)
        # send messages from protocol (protocol returns a 2D array of messages to send)
        # [Aarti]: I think we might be better off if we move this entire logic to protocol instead of keeping it
        # generic per node. Dolev Strong requires broadcast PER MESSAGE, others may not
        for i in range(len(send_messages)):
            for index, msg in enumerate(send_messages[i]):
                self.np.send_message(self.get_id(), index, msg)
    
    def get_committed_log(self):
        return self.committed_log

    def adversary_actions(self):
        # stub
        pass
