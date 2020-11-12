from common.utils import *
from network_process import NetworkProcess
from node import Node


class Main:
    def __init__(self, protocol):
        (self.num_h_nodes, self.num_a_nodes) = self.get_initialization()
        # initialize number of nodes, *nwprocess
        self.num_nodes = self.num_a_nodes + self.num_h_nodes
        self.np = NetworkProcess(self.num_nodes)

        self.h_nodes_arr = []
        self.a_nodes_arr = []

        # initialize main with the protocol object
        self.protocol = get_protocol(protocol, self.num_a_nodes, self.num_h_nodes)

        # TODO: uncomment when we have a UI component
        # self.ui = ui()

        # initialize honest nodes
        for i in range(self.num_h_nodes):
            h_node = Node(i, self.protocol, self.np)
            self.h_nodes_arr.append(h_node)

        # initialize adversary nodes
        for i in range(self.num_a_nodes):
            a_node = Node(i + self.num_h_nodes, self.protocol, self.np, adversary=True)
            self.a_nodes_arr.append(a_node)

    def get_initialization(self):
        return 2, 0  # nodes, stub

    def start_loop(self):
        while True:
            # iterate through each node and run protocol
            for i in range(self.num_h_nodes):
                self.h_nodes_arr[i].run_protocol_one_round()

            for i in range(self.num_a_nodes):
                self.a_nodes_arr[i].run_protocol_one_round()

            # call adversary actions
            for i in range(self.num_a_nodes):
                self.a_nodes_arr[i].adversary_actions()

            self.protocol.round += 1

            # TODO: uncomment when we have UI component
            # self.ui.update() # Might need to take in nodes, messages
            input()

            self.np.empty_messages()


if __name__ == '__main__':
    # TODO: this is hard-coded for now, make this a user-input
    protocol_chosen = DOLEV_STRONG_PROTOCOL
    m = Main(protocol_chosen)
    m.start_loop()
