from abc import ABC


class protocol (ABC):
    
    @abstractmethod
    def __init__ (self):
        #stub
    
    @abstractmethod
    def run (self, received_messages):
        return []

