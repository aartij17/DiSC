import pandas as pd
import networkx as nx
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import threading
import time
fig = plt.figure(figsize=(12, 8))



class UI:

    def __init__(self, inboxes):
        #stub
        self.num_nodes = len(inboxes)
        self.inboxes = inboxes
        self.sem = threading.Semaphore()

    def draw(self):
        From = []
        To = []
        pos = {}  # Node positionss
        NodeColors = {}
        for i in range(self.num_nodes):
            node_name = "Node " + str(i) + " Inbox"
            pos[node_name] = (i, 1)
            message_idx = 0
            NodeColors[node_name] = [1, .5, 1]
            from_node = node_name
            for message in self.inboxes[i]:
                if len(message) > 0:
                    message_idx += 1
                    node_message = str(message_idx) + ":" + message
                    NodeColors[node_message] = [1, 1, 0]
                    pos[node_message] = (i, message_idx + 1)
                    From.append(from_node)
                    To.append(node_message)
                    from_node = node_message

        # print("From", From)
        # print("To", To)
        # print(pos)

        df = pd.DataFrame({'from': From,
                        'to': To})

        Labels = {}
        for a in From:
            Labels[a] = a
        for b in To:
            Labels[b] = b
        # print("Labels", Labels)

        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())
        Circles = []
        Colors = []
        for n in G.nodes:
            Circles.append(n)
            Colors.append(NodeColors[n])

        nodes = nx.draw_networkx_nodes(G, pos,
                                    nodelist=Circles,
                                    node_size=1.25e3,
                                    node_shape='o',
                                    node_color='white',
                                    alpha=0)

        nodes = nx.draw_networkx_nodes(G, pos,
                                    nodelist=Circles,
                                    node_size=1e3,
                                    node_shape='o',
                                    node_color=Colors,
                                    edgecolors='black',
                                    alpha=0.5)

        nx.draw_networkx_labels(G, pos, Labels, font_size=4)

        edges = nx.draw_networkx_edges(G, pos,
                                    node_size=1.8e3,
                                    arrowstyle='->', width=2, arrowsizes=6)
        
    def update(self):
        # self.sem.release()
        plt.clf()
        self.draw()
        plt.draw()
        plt.pause(0.001)

    def start(self):
        self.draw()
        plt.xlim(-1, self.num_nodes + 1)
        plt.ylim(0, 2 * self.num_nodes)
        plt.axis('off')
        plt.ion()
            # self.sem.acquire()
        plt.show()


if __name__ == "__main__":
    inboxes = [[], [], [], []]
    ui = UI(inboxes)
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
            ui.update()
            print(inboxes)
            time.sleep(3)


