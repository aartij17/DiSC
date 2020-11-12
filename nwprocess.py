class nwprocess:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.prev_messages_passed = []
        for i in range (num_nodes):
            self.prev_messages_passed.append ([])
            for j in range(num_nodes):
                self.prev_messages_passed.append("")
            
        self.next_messages_passed = []
        for i in range (num_nodes):
            self.next_messages_passed.append ([])
            for j in range(num_nodes):
                self.next_messages_passed.append("")
        # [ [] [] [] [] ]

    def send_message(self, send_node_id, receive_node_id, message):
        self.next_messages_passed[receive_node_id][send_node_id] = message
    
    def receive_messages(self, receive_node_id):
        return self.prev_messages_passed[receive_node_id].copy()
        
    def drop_message(self, send_node_id, receive_node_id):
        self.next_messages_passed[receive_node_id][send_node_id] = ""
    
    def empty_messages(self):
        self.prev_messages_passed = self.next_messages_passed
    
        self.next_messages_passed = []
        for i in range (self.num_nodes):
            self.next_messages_passed.append ([])
            for j in range(num_nodes):
                self.next_messages_passed.append("")
    
    def num_nodes(self):
        return self.num_nodes
