from abc import ABC, abstractmethod


class ProtocolBase(ABC):
    @abstractmethod
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        self.round = 0
        self.num_faulty_nodes = num_faulty_nodes
        self.num_honest_nodes = num_honest_nodes
        self.num_nodes = self.num_faulty_nodes + self.num_honest_nodes
        pass
    
    @abstractmethod
    def run_protocol_one_round(self, state, np, log):
        return

    @abstractmethod
    def init_state(self, state):
        return
    
    @abstractmethod
    def get_protocol_name(self) -> str:
        return
