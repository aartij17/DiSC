
class Log():

    def __init__(self):
        self.log = {}
    
    
    def write(self, nodeid, value):
        if nodeid not in self.log:
            self.log[nodeid] = [ value ]
        else:
            self.log[nodeid].append(value)
    
    def read(self, nodeid, index):
        if nodeid not in self.log or index >= len(self.log[nodeid]):
            return None
        else:
            return self.log[nodeid][index]
    
    def modify(self, nodeid, index, newval):
        if nodeid not in self.log or index >= len(self.log[nodeid]):
            return False
        else:
            self.log[nodeid][index] = newval
            return True
