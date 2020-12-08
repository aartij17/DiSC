from protocols.protocol import ProtocolBase
from common.constants import *

class DoNothingAdversary(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    def run_protocol_one_round(self, state, np, log):
        return

    def init_state(self, state):
        return

    def get_protocol_name(self) -> str:
        return ADVERSARY_DONOTHING_PROTOCOL
