from protocols.protocol import ProtocolBase
from common.constants import *
from message import *
import random
import string


SIG_KEY_FORMAT = "Key:{}"

class RandomBroadcastAdversary(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    def run_protocol_one_round(self, state, np, log):
        # Broadcast a randomized string to everyone
        for i in range(np.num_nodes):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            message = Message(random_string, state["node_id"], state["round"], [])
            message.create_add_signature(SIG_KEY_FORMAT.format(state["node_id"]), message.content)
            np.send_message(i, message)

        state["round"] += 1

        return

    def init_state(self, state):
        state["round"] = 0
        return

    def get_protocol_name(self) -> str:
        return ADVERSARY_RANDOMBROADCAST_PROTOCOL
