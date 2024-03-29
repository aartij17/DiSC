# import sys
#
# from common.constants import *
# from common.signatures import *
# from message import Message
# from protocols.protocol import ProtocolBase
#
# FIRST_DOLEV_STRONG_MESSAGE = 1
# SIG_KEY_FORMAT = "Key:{}"
#
#
#
# class DolevStrongAdversary(ProtocolBase):
#     def __init__(self, num_faulty_nodes, num_honest_nodes):
#         super().__init__(num_faulty_nodes, num_honest_nodes)
#         self.all_messages = []
#
#
#     def run_protocol_one_round(self, state, np, log):
#         # Forward every message it ever received, even if not valid, to every other node
#         self.all_messages.extend(np.receive_messages(state["node_id"]))
#         print("----------------------- round: {}, adversary node_id: {} -----------------------".format(state["round"],
#                                                                                               state["node_id"]))
#
#         send_messages = []
#         valid_rcvd_msg_content = []
#         prepared_send_messages = []
#         rcvd_message_objects = self.all_messages
#         print("***** rcvd_message_objects: {}".format(rcvd_message_objects))
#
#         for i, rcvd_msg_obj in enumerate(rcvd_message_objects):
#             print("index {} of rcvd_message_objects".format(i))
#             valid_rcvd_msg_content.append("{}".format(rcvd_msg_obj.content))
#             new_message = Message("", state["round"])
#             send_messages.append(new_message)
#         print(valid_rcvd_msg_content)
#         join_broadcast_message = MESSAGES_PER_NODE_DELIM.join(
#             valid_rcvd_msg_content)
#         for msg_obj in send_messages:
#             msg_obj.content = join_broadcast_message
#             msg_obj.create_add_signature(
#                 SIG_KEY_FORMAT.format(state["node_id"]), msg_obj.content)
#
#         for msg_obj in send_messages:
#             msg_obj.sender_id = state["node_id"]
#             prepared_send_messages.append(msg_obj)
#             # prepared_send_messages.append(msg_obj.create_message(msg_obj.round,
#             #                                                         msg_obj.content,
#             #                                                         msg_obj.signatures))
#
#         np.send_messages(prepared_send_messages, True)
#     # else:
#     #     print("Something's off!")
#
#
#     def init_state(self, state):
#         state["round"] = 0
#
#     def get_protocol_name(self) -> str:
#         return DOLEV_STRONG_ADVERSARY


from common.constants import *
from common.signatures import *
from main import log
from message import Message
from protocols.protocol import ProtocolBase

FIRST_DOLEV_STRONG_MESSAGE = 1
SIG_KEY_FORMAT = "Key:{}"


def create_message_objects(messages):
    message_obj_list = []
    for msg in messages:
        message_obj_list.append(Message.get_message_object(msg))
    return message_obj_list


class DolevStrongAdversary(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    '''
        Run receives all the messages which this node has received in the previous round
        According to Dolev Strong, the following steps are followed in each round:
        1. Validate the signatures on each message
        2. Check if the message is already part of the `committed_list`. If not, add it
        3. Append the node's own signature to the message and broadcast it to other nodes
            In this case, a 2D array is maintained to return a list of messages which are to be broadcast
            Each row contains a list of messages which are to be broadcast to the receiver node
            
        Suppose received_messages = [b1, b2, b3]
        send_messages = ["b1||b2||b3", "b1||b2||b3"]
    '''

    def run_protocol_one_round(self, state, np, l=None):
        state["received_messages"] = np.receive_messages(state["node_id"])
        log.error(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ROUND: {}, NODE_ID: {} @@@@@@@@@@@@@@@@@@@@@@@@@@@".format(state["round"],
                                                                                                     state["node_id"]))
        if state["round"] == 0 and state["node_id"] == 0:
            new_message = Message(FIRST_DOLEV_STRONG_MESSAGE, state["round"])
            new_message.create_add_signature(SIG_KEY_FORMAT.format(state["node_id"]),
                                             FIRST_DOLEV_STRONG_MESSAGE)

            log.debug("returning, since round=0: {}".format([FIRST_DOLEV_STRONG_MESSAGE] * (self.num_faulty_nodes
                                                                                            + self.num_honest_nodes)))

            new_message.sender_id = state["node_id"]
            send_messages = new_message
            state["extracted_set"].add(FIRST_DOLEV_STRONG_MESSAGE)
            np.broadcast(send_messages, False)

        elif 1 <= state["round"] < self.num_faulty_nodes - 1:
            valid_rcvd_msg_content = []
            messages_to_be_sent = []
            # log.debug("***** rcvd_message_objects: {}".format(state["received_messages"]))
            for i, r_msg in enumerate(state["received_messages"]):
                verified = self.verify_message_signatures(r_msg, state)
                if not verified:
                    log.critical("Invalid signature found, ignoring the message: {}".format(r_msg))
                    # state["round"] += 1
                    continue

                valid_rcvd_msg_content.append("{}".format(r_msg.content))
                state["extracted_set"].add(r_msg.content)

                sig = create_signature(SIG_KEY_FORMAT.format(state["node_id"]), r_msg.content)

                if (sig not in r_msg.signatures):
                    new_message = Message(r_msg.content, state["node_id"], state["round"], r_msg.signatures.copy())
                    new_message.create_add_signature(SIG_KEY_FORMAT.format(state["node_id"]), r_msg.content)
                    messages_to_be_sent.append(new_message)

            if state["round"] < self.num_faulty_nodes - 1 and len(messages_to_be_sent) > 0:
                np.broadcast(messages_to_be_sent, True)

                # new_message = Message(r_msg.content, state["node_id"], state["round"], r_msg.signatures.copy())
                # new_message.create_add_signature(SIG_KEY_FORMAT.format(state["node_id"]), r_msg.content)
                # messages_to_be_sent.append(new_message)

            # np.broadcast(messages_to_be_sent, True)

        elif state["round"] == self.num_faulty_nodes - 1:
            import random
            import string
            signatures = []
            msg = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            for id in range(self.num_honest_nodes, self.num_nodes):
                signatures.append(create_signature(SIG_KEY_FORMAT.format(id), msg))
            msg = Message(msg, state["node_id"], state["round"], signatures)
            np.send_message(0, msg, False)

        # if state["round"] == self.num_faulty_nodes + 1:
        #     print("current_round: {}, num_faulty_nodes: {}".format(state["round"], self.num_faulty_nodes))
        #     if len(state["extracted_set"]) == 1:
        #         print("Consensus output: {}".format(
        #             state["extracted_set"]))  # TODO: figure out what bit has to be returned
        #     else:
        #         print("Failure to achieve Consensus output: {}".format(0))
        # print("state updated:: {}".format(state["round"]))
        state["round"] = state["round"] + 1

    def init_state(self, state):
        state["round"] = 0
        state["extracted_set"] = set()
        state["known_signatures"] = []

    def get_protocol_name(self) -> str:
        return DOLEV_STRONG_PROTOCOL

    def verify_message_signatures(self, msg_obj, state):
        if not (len(set(msg_obj.signatures)) == len(msg_obj.signatures)
                and len(msg_obj.signatures) == state["round"]):
            # log.debug("len(set(msg_obj.signatures)) == len(msg_obj.signatures): {}".format(len(set(msg_obj.signatures)) == len(msg_obj.signatures)))
            # log.debug("len(msg_obj.signatures) != state[round]: {}".format(len(msg_obj.signatures) != state["round"]))
            return False
        if msg_obj.sender_id > self.num_nodes:
            return False
        for s in msg_obj.signatures:
            node_sig_verified = False
            # <b>1,2,3,4
            for i in range(self.num_nodes):
                # if i == state["node_id"]:
                #     continue
                node_sig_verified = verify_signature(SIG_KEY_FORMAT.format(i), msg_obj.content, s)
                if node_sig_verified:
                    break
            if not node_sig_verified:
                return False
        return True
