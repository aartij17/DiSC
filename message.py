import json
from common.constants import *
from common.signatures import create_signature


class Message:
    def __init__(self, content, sender_id, r=0, signatures=None):
        self.content = content
        self.sender_id = sender_id
        self.round = r
        self.signatures = signatures if signatures else []
        self.sender_id = sender_id

    def get_sender (self):
        return self.sender_id
        
    def create_message_string(self):
        return "{}{}{}{}{}{}{}".format(
            self.round,
            INTRA_MESSAGE_DELIM,
            self.sender_id,
            INTRA_MESSAGE_DELIM,
            self.content,
            INTRA_MESSAGE_DELIM,
            json.dumps(self.signatures)
        )

    @classmethod
    def create_message(cls, round, sender_id, content, signatures):
        return "{}{}{}{}{}{}{}".format(
            round,
            INTRA_MESSAGE_DELIM,
            sender_id,
            INTRA_MESSAGE_DELIM,
            content,
            INTRA_MESSAGE_DELIM
        ) + json.dumps(signatures)

    def create_add_signature(self, key, content):
        signature = create_signature(key, content)
        self.signatures.append(signature)

    def get_sender(self):
        return self.sender_id

    @classmethod
    def get_message_elements(cls, msg):
        if INTRA_MESSAGE_DELIM in msg:
            split_message = msg.split(INTRA_MESSAGE_DELIM)
            return split_message
        else:
            return [msg]

    @classmethod
    def get_message_round(cls, msg):
        return int(cls.get_message_elements(msg)[0])

    @classmethod
    def get_message_content(cls, msg):
        return msg.content

    @classmethod
    def get_message_signatures(cls, msg):
        return json.loads(msg.signatures)

    @classmethod
    def get_message_object(cls, msg):
        print(msg)
        message_elements = msg.split(INTRA_MESSAGE_DELIM)
        signatures = json.loads(message_elements[3])
        new_msg_obj = Message(
            message_elements[2],
            message_elements[1],
            r=message_elements[0],
            signatures=signatures
        )
        return new_msg_obj

    @classmethod
    def copy_message(cls, msg):
        cpy_msg = Message(msg.content, msg.get_sender(), msg.round, msg.signatures.copy())
        return cpy_msg
