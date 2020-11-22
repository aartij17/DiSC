from common.constants import *
from message import Message
from protocols.protocol import ProtocolBase


FIRST_DOLEV_STRONG_MESSAGE = "0"


def create_message_objects(messages):
    message_obj_list = []
    for msg in messages:
        message_obj_list.append(Message.get_message_object(msg))
    return message_obj_list


class DolevStrong(ProtocolBase):
    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)

    def run_protocol_one_round(self, state, np, log):
        state["received_messages"] = np.receive_messages(state["node_id"])
        #print("node ID: {}, received messages: {}".format(self.get_id(), self.received_messages))

        # send_messages, multi_message, stop = self.run(self.received_messages, self.get_id(),
        #                                                  committed_messages=self.committed_log)
        #print("send messages: ", send_messages)
        print("----------------------- round: {}, node_id: {} -----------------------".format(state["round"], state["node_id"]))
        if state["round"] == 0:# and state["node_id"] == 0:
            new_message = Message(FIRST_DOLEV_STRONG_MESSAGE, state["round"])
            new_message.create_add_signature(state["round"], state["node_id"], FIRST_DOLEV_STRONG_MESSAGE)
            print("returning, since round=0", [FIRST_DOLEV_STRONG_MESSAGE] * (self.num_faulty_nodes
                                                                                + self.num_honest_nodes))
            send_messages = [Message.create_message(new_message.round, new_message.content, new_message.signatures)] * \
                   (self.num_faulty_nodes + self.num_honest_nodes)
            np.send_messages(send_messages, False)

        elif 1 <= state["round"] <= (self.num_faulty_nodes + 1):
            print("***** SECOND IF CONDITION **********")
            send_messages = []
            valid_rcvd_msg_content = []
            prepared_send_messages = []
            rcvd_message_objects = create_message_objects(state["received_messages"])
            print("***** rcvd_message_objects: {}".format(rcvd_message_objects))
            for i, rcvd_msg_obj in enumerate(rcvd_message_objects):
                print("index {} of rcvd_message_objects".format(i))
                rcvd_msg_content = Message.get_message_content(rcvd_msg_obj)
                # TODO: check signature validity and add the content to valid_rcvd_msg_content
                if log[state["node_id"]] is not None and rcvd_msg_content in log[state["node_id"]]:
                #if rcvd_msg_content in log[state["node_id"]]:
                    print("*** CONTINUE!***")
                    continue
                valid_rcvd_msg_content.append(rcvd_msg_content)
                log.write(state["node_id"], rcvd_msg_content)
                new_message = Message("", state["round"])
                send_messages.append(new_message)
            print(valid_rcvd_msg_content)
            join_broadcast_message = MESSAGES_PER_NODE_DELIM.join(valid_rcvd_msg_content)
            for msg_obj in send_messages:
                msg_obj.content = join_broadcast_message
                msg_obj.create_add_signature(state["round"], state["node_id"], msg_obj.content)

            for msg_obj in send_messages:
                prepared_send_messages.append(msg_obj.create_message(msg_obj.round,
                                                                     msg_obj.content,
                                                                     msg_obj.signatures))

            np.send_messages(prepared_send_messages, True)
        else:
            print("Something's off!")

        print("Log: {}, State: {}".format(log[state["node_id"]], state))
        state["round"] = state["round"] + 1

        # if stop:
        #     return
        # for i in range(len(send_messages)):
        #     print("sending message, sender: {}, receiver: {}".format(self.get_id(), i))
        #     self.np.send_message(i, send_messages[i], multi_message)
        # print("Node: {}, Committed log: {}".format(self.get_id(), self.committed_log))

    def init_state(self, state):
        state["round"] = 0

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

    # def run(self, received_messages, node_id, **kwargs):#signatures=None, committed_messages=None):
    #     # the node has received a set of messages right now.
    #     # in the 0th round, sender sends <b>_0 to every node. This message has a valid signature of the
    #     # sender node
    #     #print("----------------------- round: {}, node_id: {} -----------------------".format(state["round"], node_id))
    #     if state["round"] == 0 and node_id == 0:
    #         new_message = Message(FIRST_DOLEV_STRONG_MESSAGE, state["round"])
    #         new_message.create_add_signature(state["round"], node_id, FIRST_DOLEV_STRONG_MESSAGE)
    #         print("returning, since round=0", [FIRST_DOLEV_STRONG_MESSAGE] * (self.num_faulty_nodes
    #                                                                             + self.num_honest_nodes))
    #         return [Message.create_message(new_message.round, new_message.content, new_message.signatures)] * \
    #                (self.num_faulty_nodes + self.num_honest_nodes), False, False
    #
    #     elif 1 <= state["round"] <= (self.num_faulty_nodes + 1):
    #         send_messages = []
    #         valid_rcvd_msg_content = []
    #         prepared_send_messages = []
    #         rcvd_message_objects = create_message_objects(received_messages)
    #         for i, rcvd_msg_obj in enumerate(rcvd_message_objects):
    #             rcvd_msg_content = Message.get_message_content(rcvd_msg_obj)
    #             # TODO: check signature validity and add the content to valid_rcvd_msg_content
    #             if rcvd_msg_content in kwargs["committed_messages"]:
    #                 continue
    #             valid_rcvd_msg_content.append(rcvd_msg_content)
    #             kwargs["committed_messages"].append(rcvd_msg_content)
    #             new_message = Message("", state["round"])
    #             send_messages.append(new_message)
    #         print(valid_rcvd_msg_content)
    #         join_broadcast_message = MESSAGES_PER_NODE_DELIM.join(valid_rcvd_msg_content)
    #         for msg_obj in send_messages:
    #             msg_obj.content = join_broadcast_message
    #             msg_obj.create_add_signature(state["round"], node_id, msg_obj.content)
    #
    #         for msg_obj in send_messages:
    #             prepared_send_messages.append(msg_obj.create_message(msg_obj.round,
    #                                                                  msg_obj.content,
    #                                                                  msg_obj.signatures))
    #
    #         return prepared_send_messages, True, False
    #     elif state["round"] > (self.num_faulty_nodes + 1):
    #         return [], False, True
    #     else:
    #         return [], False, False
