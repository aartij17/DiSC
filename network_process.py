from common.constants import *


class NetworkProcess:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.prev_messages_passed = []
        self.next_messages_passed = []

        # [ [] [] [] [] ]
        for i in range(num_nodes):
            self.prev_messages_passed.append([])
            self.next_messages_passed.append([])

    def send_message(self, receive_node_id, message, multi_message=False):
        if multi_message:
            messages_for_one_node = message.split(MESSAGES_PER_NODE_DELIM)
        else:
            messages_for_one_node = [message]
        for m in messages_for_one_node:
            if len(self.next_messages_passed[receive_node_id]) == 0:
                self.next_messages_passed[receive_node_id].append(m)
            else:
                self.next_messages_passed[receive_node_id] = [m]
    
    def receive_messages(self, receive_node_id):
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
