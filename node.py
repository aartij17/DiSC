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
        #print("node ID: {}, received messages: {}".format(self.get_id(), self.received_messages))

        send_messages, multi_message, stop = self.protocol.run(self.received_messages, self.get_id(),
                                                         committed_messages=self.committed_log)
        #print("send messages: ", send_messages)
        if stop:
            return
        for i in range(len(send_messages)):
            print("sending message, sender: {}, receiver: {}".format(self.get_id(), i))
            self.np.send_message(i, send_messages[i], multi_message)
        print("Node: {}, Committed log: {}".format(self.get_id(), self.committed_log))

    def get_committed_log(self):
        return self.committed_log

    def adversary_actions(self):
        # stub
        pass
