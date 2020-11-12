from protocols.protocol import ProtocolBase
from message import Message

FIRST_DOLEV_STRONG_MESSAGE = "0"


class DolevStrong(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    '''
    Run receives all the messages which this node has received in the previous round
    According to Dolev Strong, the following steps are followed in each round:
    1. Validate the signatures on each message
    2. Check if the message is already part of the `committed_list`. If not, add it
    3. Append the node's own signature to the message and broadcast it to other nodes
        In this case, a 2D array is maintained to return a list of messages which are to be broadcast
        Each row contains a list of messages which are to be broadcast to the receiver node
        
    Suppose received_messages = [b1, b2, b3]
    send_messages = [[b1, b1, b1],
                     [b2, b2, b2],
                     [b3, b3, b3]]
    '''

    def run(self, received_messages, node_id, signatures=None, committed_messages=None):
        # the node has received a set of messages right now.
        # in the 0th round, sender sends <b>_0 to every node. This message has a valid signature of the
        # sender node
        send_messages = [[]] * len(received_messages)
        print("----------------------- round: {}, node_id: {} -----------------------".format(self.round, node_id))
        if self.round == 0:  # and node_id == 0:
            message = Message(self.round, FIRST_DOLEV_STRONG_MESSAGE)
            signatures.append(message.get_new_signature())  # TODO: Add PKI signatures
            print("returning, since round=0", [[message]] * len(received_messages))
            return [[message]] * len(received_messages)

        elif 1 <= self.round <= (self.num_faulty_nodes + 1):
            # on this node, for every message received, there are r signatures from other nodes too
            for i, msg in enumerate(received_messages):
                # TODO: verify the received messages first
                content = Message.get_message_content(msg)
                # TODO: uncomment this later on
                if content in committed_messages:
                    continue
                committed_messages.append(content)
                new_message = Message(round, content)
                new_message.create_add_signature()
                messages_for_node_i = []
                for j in range(len(received_messages)):
                    messages_for_node_i.append(new_message)
                send_messages.append(messages_for_node_i)
                return send_messages
        else:
            return RuntimeError
