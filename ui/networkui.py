import pandas as pd
import networkx as nx
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import threading
import time

fig = plt.figure(figsize=(12, 8))

ui_id = 1


class NetworkUI:

    def __init__(self, data, num_nodes, num_honest_nodes, num_adversary_nodes):
        # stub
        global ui_id

        self.num_nodes = num_nodes
        self.num_honest_nodes = num_honest_nodes
        self.num_adversary_nodes = num_adversary_nodes
        self.data = data
        self.id = ui_id
        ui_id += 1

    def draw(self):
        From = []
        To = []
        pos = {}  # Node positions
        NodeColors = {}

        for i in range(self.num_nodes):
            #recv_node_name = "Receiver: Node " + str(i)
            recv_node_name = str(i)
            pos[recv_node_name] = (i, 1)
            message_idx = 0
            color_triple = [1, 0.5, 1]
            if i >= self.num_honest_nodes:
                color_triple = [1, 0, 0]
            NodeColors[recv_node_name] = color_triple
            for j in range(len(self.data[i])):
                message = self.data[i][j]
                inner_color_triple = [1, 0.5, 1]
                if message is not None and type(message) != str:
                    #sender_node_name = "Sender: Node " + str(message.get_sender())
                    sender_node_name = str(message.get_sender()) + " "
                    if int(message.get_sender()) >= self.num_honest_nodes:
                        inner_color_triple = [1, 0, 0]
                    #sender_node_name = "Sender: Node " + str(message.get_sender())
                    if sender_node_name not in pos:
                        pos[sender_node_name] = (j, 3)
                        NodeColors[sender_node_name] = inner_color_triple
                        
                    message_idx += 1
                    NodeColors[message] = [1, 1, 0]
                    if message not in pos:
                        pos[message] = (message_idx, 2)
                    From.append(sender_node_name)
                    To.append(message)
                    From.append(message)
                    To.append(recv_node_name)

        df = pd.DataFrame({'from': From,
                           'to': To})

        Labels = {}
        for a in From:
            Labels[a] = a
        for b in To:
            Labels[b] = b

        G = nx.from_pandas_edgelist(
            df, 'from', 'to', create_using=nx.DiGraph())
        Circles = []
        Colors = []
        for n in G.nodes:
            Circles.append(n)
            Colors.append(NodeColors[n])

        nodes = nx.draw_networkx_nodes(G, pos,
                                       nodelist=Circles,
                                       node_size=2e3,
                                       node_shape='o',
                                       node_color='white',
                                       alpha=0)

        nodes = nx.draw_networkx_nodes(G, pos,
                                       nodelist=Circles,
                                       node_size=2e3,
                                       node_shape='o',
                                       node_color=Colors,
                                       edgecolors='black',
                                       alpha=0.5)

        nx.draw_networkx_labels(G, pos, Labels, font_size=10)

        edges = nx.draw_networkx_edges(G, pos,
                                       node_size=1.8e3,
                                       arrowstyle='->', width=2)  # , arrowsizes=6)

    def replace_data(self, new_data, new_num_nodes):
        self.data = new_data
        self.num_nodes = new_num_nodes

    def update(self):
        plt.figure(self.id)
        plt.clf()
        self.draw()
        plt.draw()
        plt.pause(0.001)

    def start(self):
        plt.figure(self.id)
        self.draw()
        plt.xlim(-1, self.num_nodes + 1)
        plt.ylim(0, 2 * self.num_nodes)
        plt.axis('off')
        plt.ion()
        plt.show()


if __name__ == "__main__":
    inboxes = [[], [], [], []]

    ui = NetworkUI(inboxes, len(inboxes))
    ui.start()


    test_message_inbox = [
        ["message1", "message2", "message3", "message12"],
        ["message5", "message6", "message7", ""],
        ["message8", "", "", "message11"],
        ["", "message9", "message10", ""]
    ]

    for i in range(len(test_message_inbox)):
        for j in range(len(test_message_inbox[i])):
            inboxes[i].append(test_message_inbox[i][j])
            # logs.write(i, test_message_inbox[i][j])
            ui.update()
            # logui.update()
            print(inboxes)
            time.sleep(3)
