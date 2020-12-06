from protocols.protocol import ProtocolBase
from common.constants import *
from message import *
import random
import string

class RandomBroadcastAdversary(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    def run_protocol_one_round(self, state, np, log):
        # Broadcast a randomized string to everyone
        for i in range(np.num_nodes()):
            
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            message = Message.create_message(state["round"], state["node_id"], random_string, [])
            np.send_message(i, random_string)
        return

    def init_state(self, state):
        return

    def get_protocol_name(self) -> str:
        return ADVERSARY_RANDOMBROADCAST_PROTOCOL
