
from common.log import *
from common.utils import *
from network_process import NetworkProcess
from ui.networkui import NetworkUI
from node import Node
import os
import datetime
import json
import sys


class Main:
    def __init__(self, protocol):
        (self.num_h_nodes, self.num_a_nodes) = self.initialize_number_of_nodes()
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
            adversary_protocol = get_protocol(config_blob["adversary_nodes"][i], self.num_a_nodes, self.num_h_nodes)
            a_node = Node(i + self.num_h_nodes, adversary_protocol, self.np, self.log, adversary=True)
            self.a_nodes_arr.append(a_node)

    def start_loop(self):
        counter = 0
        prev_ui = NetworkUI(self.np.prev_messages_passed, len(self.np.prev_messages_passed))
        next_ui = NetworkUI(self.np.next_messages_passed, len(self.np.next_messages_passed))
        prev_ui.start()
        next_ui.start()

        current_path = os.getcwd()
        directory_name =  os.path.join(current_path, 'run_' + str(datetime.datetime.now()))
        os.makedirs(directory_name)
        
        f_states = open(os.path.join(directory_name,"state_dump.txt"), 'w')
        f_np = open(os.path.join(directory_name, "np_dump.txt"), 'w')
        f_conf = open(os.path.join(directory_name,"config_dump.txt"), 'w')
        f_conf.write(json.dumps({
            'Honest nodes': len(self.h_nodes_arr),
            'Adversary nodes': len(self.a_nodes_arr),
            'Protocol': self.protocol.get_protocol_name()
        }))
        f_conf.close()
        while True:  # counter < 3:
            user_input = input("Enter any key to start next round, enter q to exit\n")
            if user_input == 'q':
                f_states.close()
                return

            # iterate through each node and run protocol
            for i in range(self.num_h_nodes):
                self.h_nodes_arr[i].run_protocol_one_round()

            for i in range(self.num_a_nodes):
                self.a_nodes_arr[i].run_protocol_one_round()

            # # call adversary actions
            # for i in range(self.num_a_nodes):
            #     self.a_nodes_arr[i].adversary_actions()

            # self.protocol.round += 1


            prev_ui.replace_data(self.np.prev_messages_passed, len(self.np.prev_messages_passed))
            prev_ui.update()
            next_ui.replace_data(self.np.next_messages_passed, len(self.np.next_messages_passed))
            next_ui.update()

            # f_np.write(str(counter) + "|PrevMessages|" + json.dumps(self.np.prev_messages_passed) + "\n")
            # f_np.write(str(counter) + "|NextMessages|" + json.dumps(self.np.next_messages_passed) + "\n")

            self.np.empty_messages()
            counter += 1

            for node in self.h_nodes_arr:
                f_states.write(str(counter) + "|" + str(node.get_id()) + "|" + node.dump_state() + "\n")

            for node in self.a_nodes_arr:
                f_states.write(str(counter) + "|" + str(node.get_id()) + "|" + node.dump_state() + "\n")

        f_np.close()

    def initialize_number_of_nodes(self):
        if interactive_input:
            honest_nodes = input("Enter number of honest nodes: ")
            honest_nodes = int(honest_nodes)
            adversary_nodes = input("Enter number of adversary nodes: ")
            adversary_nodes = int(adversary_nodes)
        else:
            honest_nodes = int(config_blob["honest_nodes"])
            adversary_nodes = len(config_blob["adversary_nodes"])

        if adversary_nodes > honest_nodes:
            print("Adversary nodes cannot be more than honest nodes to achieve consensus, exiting now")
            sys.exit(1)
        return honest_nodes, adversary_nodes


interactive_input = False
config_blob = {}

if __name__ == '__main__':
    f = open("config.json")
    lines = f.read()
    config_blob = json.loads(lines)
    user_interact = input("How would you like to input?\n1. File(config.json)\n2. Interactive input\n")
    if user_interact == "1":
        protocol_chosen = config_blob["protocol"]
    else:
        interactive_input = True
        while True:
            protocol_chosen = input("Choose your protocol:\n1. Dolev Strong\n2. Streamlet\n")
            if protocol_chosen == '1':
                protocol_chosen = DOLEV_STRONG_PROTOCOL
                break
            elif protocol_chosen == '2':
                protocol_chosen = STREAMLET_PROTOCOL
                break
            else:
                print("Please enter the correct protocol choice as numbers")
                continue
    m = Main(protocol_chosen)
    m.start_loop()
