import json
from common.constants import *
from common.signatures import create_signature


class Message:
    def __init__(self, content, r=0):
        self.content = content
        self.round = r
        self.signatures = []

    def get_new_signature(self, r, node_id, message_content):
        return create_signature("{}-{}".format(r, node_id), message_content)

    def create_message(self):
        return "{}{}{}{}{}".format(
            self.round,
            INTRA_MESSAGE_DELIM,
            self.content,
            INTRA_MESSAGE_DELIM,
            json.dumps(self.signatures)
        )

    def add_signature(self, signature):
        self.signatures.append(signature)

    def create_add_signature(self, round, node_id, content):
        signature = self.get_new_signature(round, node_id, content)
        self.add_signature(signature)

    @classmethod
    def get_message_elements(cls, msg):
        split_message = msg.content.split(INTRA_MESSAGE_DELIM)
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
