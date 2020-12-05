
import sys

from common.constants import *
from common.signatures import *
from common.hash import *
from message import Message
from protocols.protocol import ProtocolBase
from protocols.streamlet_blockchain import *


# Also need a way to get ledger from user and other memory

class Streamlet (ProtocolBase):

    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)
    
    """
    def __init__ (self):
        state["proposer"] = False
        state["phase"] = 0
        # if proposer phase, then state["phase"] = 0
        # if vote phase, then state["phase"] = 1
        
        state["epoch"] = 1
        # get num nodes stub
        self.num_nodes = 5
        state["node_id"] = 0
        
        self.votes = {}
    """
        
    def get_protocol_name(self) -> str:
        return STREAMLET_PROTOCOL


    def init_state(self, state):
        state["epoch"] = 0
        state["round"] = 0
        state["blockchain"] = StreamletBlockchain()
        state["proposals"] = {}
        state["vote"] = {}
        state["proposer"] = False
        state["phase"] = 0

    
    def sort_messages (self, received_messages):
        proposal_messages = []
        vote_messages = []
        echo_messages = []
        
        for i in range (len(received_messages)):
            print (received_messages[i])
            m = Message.get_message_object (received_messages[i])
            message = m
            #print ("MESSAGE GET CONTENT")
            #print (Message.get_message_content(m))
            contents = Message.get_message_content(m).split("`")
            
            #print ("CONTENTS")
            #print (contents)
            #contents = message.split(";")
            if contents[0] == "proposal":
                proposal_messages.append (message)
            elif contents[0] == "vote":
                vote_messages.append (message)
            #elif contents[0] == "echo":
            #    for echo
            #    echo_messages[i].append (message)
        return (proposal_messages, vote_messages, echo_messages)
        
        
    
    def run_protocol_one_round(self, state, np, log):
        received_messages = np.receive_messages(state["node_id"])
        # 1-D array?
        
        #print (received_messages)
        state["received_messages"] = received_messages
        blockchain = state["blockchain"]
        
        
        sorted_messages = self.sort_messages(received_messages)
        print (sorted_messages)
        prop_mess, vote_mess, echo_mess = sorted_messages
        
        if state["phase"] == 0: # proposal phase
            hash = hash_function ("epoch_" + str (state["epoch"]))
            
            # Not quite right ???
            print ("hash%num_nodes " + str(hash % self.num_nodes))
            print ("state[node_id] " + str(state["node_id"]))
            if (hash % self.num_nodes == state["node_id"]):
                state["proposer"] = True
            else:
                state["proposer"] = False
            
            if (state["proposer"]):
                # get previous hash
                longest_blockchain_blocks = blockchain.most_depth_blocks()
                prev_hash = StreamletBlock.block_hash(longest_blockchain_blocks[0])
                # get transactions
                transactions = "STUB" + str (self.round) #input()
                proposal = StreamletBlock.static_stringify(prev_hash, state["epoch"], transactions)
                signature = create_signature ("key_" + str(state["node_id"]), proposal)
                m = Message ("proposal`" + proposal, state["node_id"], self.round, [signature])
                #send_message = "proposal;" + state["node_id"] + ";" + proposal + ";" + signature
                np.send_messages ([m.create_message_string()] * self.num_nodes, False) # supposed to be a broadcast
                # send
                    
            #state["phase"] = 1
            
        elif state["phase"] == 1: # receiving and voting for proposal phase
            print (" PHASE = 1 ===================" )
            print ("state[node_id] " + str(state["node_id"]))
            print (not state["proposer"])
            if (not state["proposer"]):
                self.handle_proposals (prop_mess, state, np)
                    
         
        # on receipt of 2/3 majority of votes, then notarize (should listen here for votes)
        elif state["phase"] == 2: # receiving votes and notarizing on the blockchain
            self.handle_votes (vote_mess)
         
        # echo proposals
        # cut corners
        # echo votes
        
        print (" ROUND = " + str (state["round"] ))
        print (" epoch = " + str (state["epoch"] ))
        print (" phase = " + str (state["phase"] ))
        
        state["round"] = state["round"] + 1
        state["epoch"] = int(state["round"] / 3)
        state["phase"] = state["round"] % 3
        
        #print (" new ROUND = " + str (state["round"] ))
        #print (" new epoch = " + str (state["epoch"] ))
        #print (" new phase = " + str (state["phase"] ))
        
    def vote(self, state, np, proposal):
        # broadcast vote to everyone
        # add vote to own counter
        prop_contents = proposal.split(",")
        prev_hash = prop_contents[0]
        epoch = prop_contents[1]
        trans = prop_contents[2]
        prop_str = StreamletBlock.static_stringify(prev_hash, epoch, trans)
        
        signature = create_signature ("key_" + str(state["node_id"]), prop_str)
        
        m = Message ("vote`" + proposal, state["node_id"], self.round, [signature])
        
        # broadcast message
        np.send_messages ([m.create_message_string()] * self.num_nodes, False)
     

    def handle_votes (self, vote_mess):

        for vot in vote_mess:
            messages = Message.get_message_content(vot).split("`")
            proposal = messages[1]
            voter = vot.get_sender()
            
            prop_contents = proposal.split(",")
            prev_hash = prop_contents[0]
            epoch = prop_contents[1]
            trans = prop_contents[2]
            
            if (verify_signature("key_" + str(state["node_id"]), proposal, Message.get_message_signatures(vot)[0])):
                if not proposal in state["proposals"]:
                    state["proposals"][proposal] = False
                if not proposal in state["votes"]:
                    state["votes"][proposal] = 1
                else:
                    state["votes"][proposal] += 1
                    
                if (state["votes"][proposal] > 2 * (self.num_faulty_nodes + self.num_honest_nodes) / 3 + 1 and not state["proposals"][proposal]):
                    state["proposals"][proposal]  = True
                    state["blockchain"].append_to_blockchain (prev_hash, epoch, trans)
                    
            
            

    def handle_proposals (self, prop_mess, state, np):
        print ("PROP MESS LEN")
        print (len (prop_mess))
        for prop in prop_mess:
            # add to proposal state
            print ("PROP ^^^^^^^")
            print (prop)
            
            accept_prop = True
        
            #contents = Message.get_message_content(prop).split(",")
            prop_id = prop.get_sender()
            proposal = Message.get_message_content(prop).split("`")[1]
            signature = Message.get_message_signatures(prop)[0]
            
            state["proposals"][proposal] = False
            
            print ("Accept proposal 1 " + str (accept_prop))
            
            #print (proposal)
            #print (signature)
            if (not verify_signature ("key_" + prop_id, proposal, signature)):
                accept_prop = False
            
            prop_contents = proposal.split(",")
            prev_hash = prop_contents[0]
            epoch = prop_contents[1]
            trans = prop_contents[2]
            
            print ("Accept proposal 2 " + str (accept_prop))
            
            if (not state["blockchain"].vote_for (prev_hash)):
                accept_prop = False
            
            print ("Accept proposal 3 " + str (accept_prop))
            
            curr_leader = hash_function("epoch_" + str(epoch)) % self.num_nodes
            if (curr_leader != prop_id):
                accept_prop = False
                
            print ("Accept proposal 4 " + str (accept_prop))
            if (accept_prop):
                self.vote(state, np, proposal)
"""
class SendMessages:
    def __init__ (self, num_nodes):
        self.arr = [""] * num_nodes
    
    def add_message (self, node, message):
        if self.arr[node] == "":
            self.arr[node] = message
        else:
            self.arr[node] += "`" + message
    
    def send_messages (self, np):
        # send messages
        
"""
