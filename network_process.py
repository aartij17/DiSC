from common.constants import *
from message import *


class NetworkProcess:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.prev_messages_passed = []
        self.next_messages_passed = []

        # [ [] [] [] [] ]
        for i in range(num_nodes):
            self.prev_messages_passed.append([])
            self.next_messages_passed.append([])

    def send_messages(self, messages, multi_message):
        print("***** SEND MESSAGES **********")
        for i in range(len(messages)):
            self.send_message(i, messages[i], multi_message)

    def send_message(self, receive_node_id, message, multi_message=False):

        message_elements = Message.get_message_elements(message)
        messages_to_be_sent = []
        if multi_message:
            messages_for_one_node = message_elements[1].split(MESSAGES_PER_NODE_DELIM)
        else:
            messages_for_one_node = message_elements[1]
        for m in messages_for_one_node:
            messages_to_be_sent.append(Message.create_message(message_elements[0],  # round
                                                              m,  # content
                                                              message_elements[2]))  # signatures

        print("messages sent out by network process: {}", format(messages_to_be_sent))
        for m in messages_to_be_sent:
            if len(self.next_messages_passed[receive_node_id]) == 0:
                self.next_messages_passed[receive_node_id] = [m]
            else:
                self.next_messages_passed[receive_node_id].append(m)

    def receive_messages(self, receive_node_id):
        print("return from receive message:", self.prev_messages_passed[receive_node_id])
        return self.prev_messages_passed[receive_node_id].copy()

    def drop_message(self, send_node_id, receive_node_id):
        self.next_messages_passed[receive_node_id][send_node_id] = ""

    def empty_messages(self):
        self.prev_messages_passed = self.next_messages_passed

        self.next_messages_passed = []
        for i in range(self.num_nodes):
            self.next_messages_passed.append([])

    def num_nodes(self):
        return self.num_nodes
