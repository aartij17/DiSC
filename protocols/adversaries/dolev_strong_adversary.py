import sys

from common.constants import *
from common.signatures import *
from message import Message
from protocols.protocol import ProtocolBase

FIRST_DOLEV_STRONG_MESSAGE = 1
SIG_KEY_FORMAT = "Key:{}"



class DolevStrongAdversary(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)
        self.all_messages = []
    

    def run_protocol_one_round(self, state, np, log):
        # Forward every message it ever received, even if not valid, to every other node
        self.all_messages.extend(np.receive_messages(state["node_id"]))
        print("----------------------- round: {}, adversary node_id: {} -----------------------".format(state["round"],
                                                                                              state["node_id"]))

        send_messages = []
        valid_rcvd_msg_content = []
        prepared_send_messages = []
        rcvd_message_objects = self.all_messages
        print("***** rcvd_message_objects: {}".format(rcvd_message_objects))

        for i, rcvd_msg_obj in enumerate(rcvd_message_objects):
            print("index {} of rcvd_message_objects".format(i))
            valid_rcvd_msg_content.append("{}".format(rcvd_msg_obj.content))
            new_message = Message("", state["round"])
            send_messages.append(new_message)
        print(valid_rcvd_msg_content)
        join_broadcast_message = MESSAGES_PER_NODE_DELIM.join(
            valid_rcvd_msg_content)
        for msg_obj in send_messages:
            msg_obj.content = join_broadcast_message
            msg_obj.create_add_signature(
                SIG_KEY_FORMAT.format(state["node_id"]), msg_obj.content)

        for msg_obj in send_messages:
            msg_obj.sender_id = state["node_id"]
            prepared_send_messages.append(msg_obj)
            # prepared_send_messages.append(msg_obj.create_message(msg_obj.round,
            #                                                         msg_obj.content,
            #                                                         msg_obj.signatures))

        np.send_messages(prepared_send_messages, True)
    # else:
    #     print("Something's off!")


    def init_state(self, state):
        state["round"] = 0

    def get_protocol_name(self) -> str:
        return DOLEV_STRONG_ADVERSARY
