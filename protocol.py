from abc import ABC, abstractmethod


class Protocol(ABC):
    @abstractmethod
    def __init__(self):
        self.round = 0
        pass
    
    @abstractmethod
    def run(self, received_messages):
        return []
