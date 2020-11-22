import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)

class Node:
    def __init__(self, node_id, protocol, np, log, adversary=False):
        self.state = {}
        self.protocol = protocol
        self.np = np
        self.log = log

        self.id = node_id

        self.received_messages = []
        self.committed_log = []

        self.adversary = adversary
        self.signatures = set()

        self.state["node_id"] = self.id
        self.state["received_messages"] = self.received_messages
        self.protocol.init_state(self.state)

    def get_id(self):
        return self.id

    def run_protocol_one_round(self):
        print("Node state before protocol run: {}".format(self.state))
        self.protocol.run_protocol_one_round(self.state, self.np, self.log)
        print("Node state after protocol run: {}".format(self.state))
        # # store messages in local memory
        # self.received_messages = []
        #
        # # received_messages is a list of messages which this node i received
        # # these messages are processed by the protocol
        # self.received_messages = self.np.receive_messages(self.get_id())
        # #print("node ID: {}, received messages: {}".format(self.get_id(), self.received_messages))
        #
        # send_messages, multi_message, stop = self.protocol.run(self.received_messages, self.get_id(),
        #                                                  committed_messages=self.committed_log)
        # #print("send messages: ", send_messages)
        # if stop:
        #     return
        # for i in range(len(send_messages)):
        #     print("sending message, sender: {}, receiver: {}".format(self.get_id(), i))
        #     self.np.send_message(i, send_messages[i], multi_message)
        # print("Node: {}, Committed log: {}".format(self.get_id(), self.committed_log))

    def get_committed_log(self):
        return self.committed_log

    def adversary_actions(self):
        # stub
        pass

    
    def dump_state(self):
        return json.dumps(self.state, cls=SetEncoder)
