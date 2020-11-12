import json


class Message:
    def __init__(self, r, content):
        self.content = content
        self.round = r
        self.signatures = []

    def get_new_signature(self):
        return "abc" # TODO: return pki signature consisting of actual message and round number

    def create_message(self):
        return "{}|{}|{}".format(
            self.round,
            self.content,
            json.dumps(self.signatures)
        )

    def add_signature(self, signature):
        self.signatures.append(signature)

    def create_add_signature(self):
        signature = self.get_new_signature()
        self.add_signature(signature)

    @classmethod
    def get_message_elements(cls, msg):
        split_message = msg.split("|")
        return split_message

    @classmethod
    def get_message_round(cls, msg):
        return int(cls.get_message_elements(msg)[0])

    @classmethod
    def get_message_content(cls, msg):
        return cls.get_message_elements(msg)[1]

    @classmethod
    def get_message_signatures(cls, msg):
        return json.loads(cls.get_message_elements(msg)[2])
