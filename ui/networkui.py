import pandas as pd
import networkx as nx
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import threading
import time

fig = plt.figure(figsize=(12, 8))

ui_id = 1


class NetworkUI:

    def __init__(self, data, num_nodes):
        # stub
        global ui_id

        self.num_nodes = num_nodes
        self.data = data
        self.id = ui_id
        ui_id += 1

    def draw(self):
        From = []
        To = []
        pos = {}  # Node positionss
        NodeColors = {}

        for i in range(self.num_nodes):
            sender_node_name = "Sender: Node " + str(i)
            pos[sender_node_name] = (i, 1)
            message_idx = 0
            NodeColors[sender_node_name] = [1, .5, 1]
            for j in range(len(self.data[i])):
                message = self.data[i][j]
                if len(message) > 0:
                    receiver_node_name = "Receiver: Node " + str(j)
                    if receiver_node_name not in pos:
                        pos[receiver_node_name] = (j, 3)
                        NodeColors[receiver_node_name] = [1, .5, 1]
                        
                    message_idx += 1
                    NodeColors[message] = [1, 1, 0]
                    if message not in pos:
                        pos[message] = (message_idx, 2)
                    From.append(sender_node_name)
                    To.append(message)
                    From.append(message)
                    To.append(receiver_node_name)

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

        nx.draw_networkx_labels(G, pos, Labels, font_size=4)

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
    # logs = Log()
    # for i in range(4):
    #     logs.write(i, "Log_" + str(i))
    inboxes = [[], [], [], []]

    ui = NetworkUI(inboxes, len(inboxes))
    ui.start()

    # logui = UI(logs, 4)
    # logui.start()

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
