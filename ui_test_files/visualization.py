import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))

test_message_inbox = [
    ["message1", "message2", "message3", "message12"],
    ["message5", "message6", "message7", ""],
    ["message8", "", "", "message11"],
    ["", "message9", "message10", ""]
]

num_nodes = 4

From = []
To = []
pos = {} # Node positionss
NodeColors = {}
for i in range(num_nodes):
    node_name = "Node " + str(i) + " Inbox"
    pos[node_name] = (i, 1)
    message_idx = 0
    NodeColors[node_name] = [1, .5, 1]
    from_node = node_name
    for message in test_message_inbox[i]:
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


# nodes = nx.draw_networkx_nodes(G, pos,
#                                nodelist=Circles,
#                                node_size=1.25e4,
#                                node_shape='>',
#                                node_color='white',
#                                alpha=1)

# nodes = nx.draw_networkx_nodes(G, pos,
#                                nodelist=Circles,
#                                node_size=1e4,
#                                node_shape='>',
#                             #    node_color=Colors,
#                                edgecolors='black',
#                                alpha=0.5)

nx.draw_networkx_labels(G, pos, Labels, font_size=4)

edges = nx.draw_networkx_edges(G, pos, 
                                node_size=1.8e3,
                                arrowstyle='->', width=2, arrowsizes=6)

plt.xlim(-1, num_nodes + 1)
plt.ylim(0, 2 * num_nodes)
plt.axis('off')
plt.show()
