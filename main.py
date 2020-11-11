from nwprocess import nwprocess
from protocol import Protocol
from node import node
from constants import *
from utils import *


class main:
    def __init__(self, protocol):
        (self.num_h_nodes, self.num_a_nodes) = self.get_initialization()
        # initialize number of nodes, *nwprocess
        self.num_nodes = self.num_a_nodes + self.num_h_nodes
        self.np = nwprocess(self.num_nodes)

        self.h_nodes_arr = []
        self.a_nodes_arr = []

        # initialize main with the protocol object
        self.protocol = get_protocol(protocol)

        # TODO: uncomment when we have a UI component
        # self.ui = ui()

        # initialize honest nodes
        for i in range(self.num_h_nodes):
            h_node = node(i, self.protocol, self.np)
            self.h_nodes_arr.append(h_node)

        # initialize adversary nodes
        for i in range(self.num_a_nodes):
            a_node = node(i + self.num_h_nodes, self.protocol, self.np, adversary=True)
            self.a_nodes_arr.append(a_node)

    def get_initialization(self):
        return 5, 0  # nodes, stub

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
            # TODO: uncomment when we have UI component
            # self.ui.update() # Might need to take in nodes, messages
            input()

            self.np.empty_messages()


if __name__ == '__main__':
    # TODO: this is hard-coded for now, make this a user-input
    protocol_chosen = DOLEV_STRONG_PROTOCOL
    m = main(protocol_chosen)
    m.start_loop()
