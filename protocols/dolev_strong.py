import sys

from common.constants import *
from common.signatures import *
from message import Message
from protocols.protocol import ProtocolBase

FIRST_DOLEV_STRONG_MESSAGE = 1
SIG_KEY_FORMAT = "Key:{}"


def create_message_objects(messages):
    message_obj_list = []
    for msg in messages:
        message_obj_list.append(Message.get_message_object(msg))
    return message_obj_list


def verify_message_signatures(round, node_id, msg_obj):
    if len(msg_obj.signatures) != round:
        print(msg_obj.signatures)
        print("VERIFY_MESSAGE_SIG:, num_sig{} != round{}".format(len(msg_obj.signatures), round))
        return False
    print("SIGNATURES: {}".format(type(msg_obj.signatures)))
    for s in msg_obj.signatures:
        print("S::: {}".format(s))
        key = SIG_KEY_FORMAT.format(node_id)
        if not verify_signature(key, msg_obj.content, s):
            return False
    return True


class DolevStrong(ProtocolBase):
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

    def run_protocol_one_round(self, state, np, log):
        state["received_messages"] = np.receive_messages(state["node_id"])
        print("----------------------- round: {}, node_id: {} -----------------------".format(state["round"],
                                                                                              state["node_id"]))
        if state["round"] == 0 and state["node_id"] == 0:
            new_message = Message(FIRST_DOLEV_STRONG_MESSAGE, state["round"])
            new_message.create_add_signature(SIG_KEY_FORMAT.format(state["node_id"]),
                                             FIRST_DOLEV_STRONG_MESSAGE)

            print("returning, since round=0", [FIRST_DOLEV_STRONG_MESSAGE] * (self.num_faulty_nodes
                                                                              + self.num_honest_nodes))

            new_message.sender_id = state["node_id"]
            send_messages = [new_message] * (self.num_nodes)
            np.send_messages(send_messages, False)

        elif 1 <= state["round"] < (self.num_faulty_nodes + 1):
            send_messages = []
            valid_rcvd_msg_content = []
            prepared_send_messages = []
            print("***** rcvd_message_objects: {}".format(state["received_messages"]))

            for i, r_msg in enumerate(state["received_messages"]):
                verified = verify_message_signatures(state["round"], state["node_id"], r_msg)
                if not verified:
                    print("Invalid signature found, terminating the protocol run")
                    sys.exit(1)

                if r_msg.content in state["extracted_set"]:
                    continue
                valid_rcvd_msg_content.append("{}".format(r_msg.content))
                state["extracted_set"].add(r_msg.content)

                new_message = Message("", state["node_id"], state["round"])
                send_messages.append(new_message)

            join_broadcast_message = MESSAGES_PER_NODE_DELIM.join(valid_rcvd_msg_content)
            for msg_obj in send_messages:
                msg_obj.content = join_broadcast_message
                msg_obj.create_add_signature(SIG_KEY_FORMAT.format(state["node_id"]), msg_obj.content)

            for msg_obj in send_messages:
                msg_obj.sender_id = state["node_id"]
                prepared_send_messages.append(msg_obj)

            np.send_messages(prepared_send_messages, True)


        state["round"] = state["round"] + 1
        if state["round"] + 1 == self.num_faulty_nodes + 2:
            if len(state["extracted_set"]) == 1:
                print("Consensus output: {}".format(
                    state["extracted_set"]))  # TODO: figure out what bit has to be returned
            else:
                print("Failure to achieve Consensus output: {}".format(0))
            # TODO: Right now, we just exit out from here. Gotta see what to do here when the input is from the file
            sys.exit(0)
        print("state updated:: {}".format(state["round"]))

    def init_state(self, state):
        state["round"] = 0
        state["extracted_set"] = set()
        state["known_signatures"] = []


    def get_protocol_name(self) -> str:
        return DOLEV_STRONG_PROTOCOL
