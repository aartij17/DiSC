from common.constants import *
from message import *


class NetworkProcess:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.prev_messages_passed = []
        self.next_messages_passed = []

        for i in range(num_nodes):
            self.prev_messages_passed.append([])
            self.next_messages_passed.append([])

    def broadcast(self, message, multi_message):
        print("******************** BROADCAST MESSAGES *************************")
        if multi_message:
            for msg in message:
                for i in range(self.num_nodes):
                    self.send_message(i, msg, False)
        else:
            for i in range(self.num_nodes):
                self.send_message(i, message, multi_message)


    def send_messages(self, messages, multi_message):
        print("******************** SEND MESSAGES *************************")
        for i in range(len(messages)):
            self.send_message(i, messages[i], multi_message)

    def send_message(self, receive_node_id, message, multi_message=False):
        #print("******************** SEND MESSAGE *************************")
        messages_to_be_sent = []
        if multi_message:
            message_content_for_one_node = message.content.split(MESSAGES_PER_NODE_DELIM)
        else:
            message_content_for_one_node = [message.content]
        for m in message_content_for_one_node:
            messages_to_be_sent.append(Message(m, message.sender_id, message.round, message.signatures))


        print("messages sent out by network process: {}".format(messages_to_be_sent))
        print("receiver id: {}".format(receive_node_id))
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
