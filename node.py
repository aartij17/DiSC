import json


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


class Node:
    def __init__(self, node_id, protocol, np, log, adversary=False):
        self.state = {}
        self.protocol = protocol
        self.np = np
        self.log = log

        self.id = node_id

        self.received_messages = []
        self.committed_log = []

        self.adversary = adversary
        self.signatures = set()

        self.state["node_id"] = self.id
        self.state["received_messages"] = self.received_messages
        self.protocol.init_state(self.state)

    def get_id(self):
        return self.id

    def run_protocol_one_round(self):
        from main import log
        # print("Node state before protocol run: {}".format(self.state))
        self.protocol.run_protocol_one_round(self.state, self.np, self.log)
        # print("Node state after protocol run: {}".format(self.state))
        log.info("=======================================================================================")

    def get_committed_log(self):
        return self.committed_log

    def adversary_actions(self):
        # stub
        pass

    def dump_state(self):
        tmp_state = {}
        for key in self.state:  # Fix
            # log.error("state: {}".format(self.state))
            value = self.state[key]
            # log.error("is_jsonable: {}, is_jsonable_STR: {}".format(is_jsonable(value), is_jsonable(str(value))))
            if is_jsonable(value):
                tmp_state[key] = value
            elif is_jsonable(str(value)):
                tmp_state[key] = str(value)
        return json.dumps(tmp_state)
