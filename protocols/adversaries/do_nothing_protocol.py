from common.constants import *
from main import log
from protocols.protocol import ProtocolBase


class DoNothingAdversary(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    def run_protocol_one_round(self, state, np, l=None):
        log.error(
            "################################### ROUND: {}, NODE_ID: {} ###################################".format(
                state["round"], state["node_id"]))
        log.error(" -> Do Nothing")

        state["round"] += 1
        return

    def init_state(self, state):
        state["round"] = 0
        return

    def get_protocol_name(self) -> str:
        return ADVERSARY_DONOTHING_PROTOCOL
