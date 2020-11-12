from abc import ABC, abstractmethod


class ProtocolBase(ABC):
    @abstractmethod
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        self.round = 0
        self.num_faulty_nodes = num_faulty_nodes
        self.num_honest_nodes = num_honest_nodes
        pass
    
    @abstractmethod
    def run(self, received_messages, node_id, signatures=None, committed_messages=None):
        return
