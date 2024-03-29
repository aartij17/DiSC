import datetime
import logging
import os
import sys

from common.log import *
from common.utils import *
from network_process import NetworkProcess
from node import Node
from ui.networkui import NetworkUI

log = logging.getLogger('pythonConfig')


def init_logger():
    global log
    LOG_LEVEL = logging.DEBUG
    from colorlog import ColoredFormatter
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(
        "%(log_color)s%(reset)s %(log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    log = logging.getLogger('pythonConfig')
    log.setLevel(LOG_LEVEL)
    log.addHandler(stream)


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

        log.info("---------------------storage initialized:---------------------")
        log.info("pre_message_passed: {}".format(self.np.prev_messages_passed))
        log.info("next_message_passed: {}".format(self.np.next_messages_passed))

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
        next_ui = NetworkUI(self.np.next_messages_passed, len(self.np.next_messages_passed), self.num_h_nodes,
                            self.num_a_nodes)
        next_ui.start()

        current_path = os.getcwd()
        directory_name = os.path.join(current_path, 'run_' + str(datetime.datetime.now()))
        os.makedirs(directory_name)

        f_states = open(os.path.join(directory_name, "state_dump.txt"), 'w')
        f_np = open(os.path.join(directory_name, "np_dump.txt"), 'w')
        f_conf = open(os.path.join(directory_name, "config_dump.txt"), 'w')
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

            next_ui.replace_data(self.np.next_messages_passed, len(self.np.next_messages_passed))
            next_ui.update()

            str_prev_msgs = [str(m) for m in self.np.prev_messages_passed]
            str_next_msgs = [str(m) for m in self.np.next_messages_passed]

            f_np.write(str(counter) + "|PrevMessages|" + json.dumps(str_prev_msgs) + "\n")
            f_np.write(str(counter) + "|NextMessages|" + json.dumps(str_next_msgs) + "\n")

            for node in self.h_nodes_arr:
                f_states.write(str(counter) + "|" + str(node.get_id()) + "|" + node.dump_state() + "\n")

            for node in self.a_nodes_arr:
                f_states.write(str(counter) + "|" + str(node.get_id()) + "|" + node.dump_state() + "\n")

            self.np.empty_messages()
            counter += 1

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
    if len(sys.argv) == 1:
        file_name = "config.json"
    else:
        file_name = sys.argv[1]
    f = open(file_name)
    lines = f.read()
    config_blob = json.loads(lines)
    protocol_chosen = config_blob["protocol"]
    init_logger()
    m = Main(protocol_chosen)
    m.start_loop()
