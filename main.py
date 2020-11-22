from common.log import *
from common.utils import *
from network_process import NetworkProcess
from ui.networkui import NetworkUI
from node import Node
import os
import datetime
import json


class Main:
    def __init__(self, protocol):
        (self.num_h_nodes, self.num_a_nodes) = self.get_initialization()
        # initialize number of nodes, *nwprocess
        self.num_nodes = self.num_a_nodes + self.num_h_nodes
        self.np = NetworkProcess(self.num_nodes)
        f = open('input_dolev.txt', 'r')
        lines = f.readlines()
        for i, line in enumerate(lines):
            self.np.prev_messages_passed[i].extend(line.split())
        f.close()
        self.h_nodes_arr = []
        self.a_nodes_arr = []

        print("---------------------storage initialized:---------------------")
        print("pre_message_passed: {}".format(self.np.prev_messages_passed))
        print("next_message_passed: {}".format(self.np.next_messages_passed))

        # initialize main with the protocol object
        self.protocol = get_protocol(protocol, self.num_a_nodes, self.num_h_nodes)

        self.log = Log()

        # initialize honest nodes
        for i in range(self.num_h_nodes):
            h_node = Node(i, self.protocol, self.np, self.log)
            self.h_nodes_arr.append(h_node)

        # initialize adversary nodes
        for i in range(self.num_a_nodes):
            a_node = Node(i + self.num_h_nodes, self.protocol, self.np, self.log, adversary=True)
            self.a_nodes_arr.append(a_node)

    def get_initialization(self):
        return 4, 2  # nodes, stub

    def start_loop(self):
        counter = 0
        prev_ui = NetworkUI(self.np.prev_messages_passed, len(self.np.prev_messages_passed))
        next_ui = NetworkUI(self.np.next_messages_passed, len(self.np.next_messages_passed))
        prev_ui.start()
        next_ui.start()

        directory_name = './run_' + str(datetime.datetime.now())
        os.mkdir(directory_name)
        f_states = open(directory_name + "/state_dump.txt", 'w')
        f_np = open(directory_name + "/np_dump.txt", 'w')
        f_conf = open(directory_name + "/config_dump.txt", 'w')
        f_conf.write(json.dumps({
            'Honest nodes': len(self.h_nodes_arr),
            'Adversary nodes': len(self.a_nodes_arr),
            'Protocol': self.protocol.get_protocol_name()
        }))
        f_conf.close()
        while True:  # counter < 3:
            user_input = input("enter q to exit") # TODO: use a user-hint to q
            if user_input == 'q':
                return

            # iterate through each node and run protocol
            for i in range(self.num_h_nodes):
                #self.protocol.run_protocol_one_round()
                self.h_nodes_arr[i].run_protocol_one_round()

            for i in range(self.num_a_nodes):
                self.a_nodes_arr[i].run_protocol_one_round()

            # call adversary actions
            for i in range(self.num_a_nodes):
                self.a_nodes_arr[i].adversary_actions()

            #self.protocol.round += 1

            # TODO: uncomment when we have UI component
            # self.ui.update() # Might need to take in nodes, messages
            #input()
            prev_ui.replace_data(self.np.prev_messages_passed, len(self.np.prev_messages_passed))
            prev_ui.update()
            next_ui.replace_data(self.np.next_messages_passed, len(self.np.next_messages_passed))
            next_ui.update()
            
            f_np.write(str(counter) + "|PrevMessages|" + json.dumps(self.np.prev_messages_passed) + "\n")
            f_np.write(str(counter) + "|NextMessages|" + json.dumps(self.np.next_messages_passed) + "\n")

            self.np.empty_messages()
            counter += 1

            for node in self.h_nodes_arr:
                f_states.write(str(counter) + "|" + str(node.get_id()) + "|" + node.dump_state() + "\n")
            
            for node in self.a_nodes_arr:
                f_states.write(str(counter) + "|" + str(node.get_id()) + "|" + node.dump_state() + "\n")


        f_states.close()
        f_np.close()
    
if __name__ == '__main__':
    # TODO: this is hard-coded for now, make this a user-input
    protocol_chosen = DOLEV_STRONG_PROTOCOL
    m = Main(protocol_chosen)
    m.start_loop()
