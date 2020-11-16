from common.constants import *
from message import Message
from protocols.protocol import ProtocolBase


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
        send_messages = [""] * len(received_messages)
        print("----------------------- round: {}, node_id: {} -----------------------".format(self.round, node_id))
        if self.round == 0:  # and node_id == 0:
            new_message = Message(self.round, FIRST_DOLEV_STRONG_MESSAGE)
            new_message.create_add_signature(self.round, node_id, FIRST_DOLEV_STRONG_MESSAGE)
            print("returning, since round=0", [[FIRST_DOLEV_STRONG_MESSAGE]] * (self.num_faulty_nodes
                                                                                + self.num_honest_nodes))
            return [new_message] * (self.num_faulty_nodes + self.num_honest_nodes), False

        elif 1 <= self.round <= (self.num_faulty_nodes + 1):
            # on this node, for every message received, there are r signatures from other nodes too
            for i, msg in enumerate(received_messages):
                # TODO: verify the received messages first
                message_signatures = Message.get_message_signatures(msg)
                #verifiy_message_signatures()
                content = Message.get_message_content(msg)
                if content in committed_messages:
                    continue
                committed_messages.append(content)
                new_message = Message(self.round, content)
                new_message.create_add_signature(self.round, node_id, content)
                for m in range(len(send_messages)):
                    send_messages[m] = "{}{}{}".format(send_messages[m], MESSAGES_PER_NODE_DELIM, new_message)

            print("send_messages after double for:{}".format(send_messages))
            return send_messages, True
        else:
            return RuntimeError
