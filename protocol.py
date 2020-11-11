from abc import ABCMeta, abstractmethod


class protocol():
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__ (self):
        #stub
        pass
    
    @abstractmethod
    def run (self, received_messages):
        return []
