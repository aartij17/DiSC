import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import threading
import time
import tkinter as tk
import tkinter as ttk
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


from log import *

LARGE_FONT = ("Verdana", 12)
inboxes_f = Figure(figsize=(5, 5), dpi=100)

class UI:

    def __init__(self, inboxes, log):
        #stub
        self.num_nodes = len(inboxes)
        self.inboxes = inboxes
        self.log = log
        

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
        plt.show()

        # app = ConsensusSimulatorGUIapp()
        # app.mainloop()



class ConsensusSimulatorGUIapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "DiSC")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, InboxPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # button = ttk.Button(self, text="Visit Page 1",
        #                     command=lambda: controller.show_frame(PageOne))
        # button.pack()

        # button2 = ttk.Button(self, text="Visit Page 2",
        #                      command=lambda: controller.show_frame(PageTwo))
        # button2.pack()

        button3 = ttk.Button(self, text="Inbox Page",
                            command=lambda: controller.show_frame(InboxPage))
        button3.pack()

class InboxPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        
        a = inboxes_f.add_subplot(111)

        canvas = FigureCanvasTkAgg(inboxes_f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == "__main__":

    logs = Log()
    inboxes = [[], [], [], []]
    ui = UI(inboxes, logs)
    ui.start()

    # test_message_inbox = [
    #     ["message1", "message2", "message3", "message12"],
    #     ["message5", "message6", "message7", ""],
    #     ["message8", "", "", "message11"],
    #     ["", "message9", "message10", ""]
    # ]

    # for i in range(len(test_message_inbox)):
    #     for j in range(len(test_message_inbox[i])):
    #         inboxes[i].append(test_message_inbox[i][j])
    #         ui.update()
    #         print(inboxes)
    #         time.sleep(3)

    # Code to add widgets will go here...
