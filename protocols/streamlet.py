import sys

from common.constants import *
from common.signatures import *
from message import Message
from protocols.protocol import ProtocolBase
from streamlet_blockchain import *


# Also need a way to get ledger from user and other memory

class Streamlet (ProtocolBase):

    def __init__(self, num_faulty_nodes, num_honest_nodes):
        super().__init__(num_faulty_nodes, num_honest_nodes)
    
    """
    def __init__ (self):
        self.proposer = False
        self.phase = 0
        # if proposer phase, then self.phase = 0
        # if vote phase, then self.phase = 1
        
        self.epoch = 1
        # get num nodes stub
        self.num_nodes = 5
        self.id = 0
        
        self.votes = {}
    """
        
    def get_protocol_name(self) -> str:
        return STREAMLET_PROTOCOL


    def init_state(self, state):
        state["epoch"] = 0
        state["round"] = 1
        state["blockchain"] = StreamletBlockchain()

    
    def sort_messages (received_messages):
        proposal_messages = []
        vote_messages = []
        echo_messages = []
        recovery_messages = []
        
        for i in range (self.num_nodes):
            proposal_messages.append ([])
            vote_messages.append ([])
            echo_messages.append ([])
            recovery_messages.append ([])
            
            messages = received_messages[i].split("|")
            for message in messages:
                contents = message.split(";")
                if contents[0] == "proposal":
                    proposal_messages[i].append (message)
                elif contents[0] == "vote":
                    vote_messages[i].append (message)
                elif contents[0] == "echo":
                    for echo 
                    echo_messages[i].append (message)
                elif contents[0] == "recovery":
                    recovery_messages[i].append (message)
        return (proposal_messages, vote_messages, echo_messages, recovery_messages)
        
        
    def vote(self, state, np, log):
        # broadcast vote to everyone
        # add vote to own counter
        # stub
        
    
    def run_protocol_one_round(self, state, np, log):
        state["received_messages"] = np.receive_messages(state["node_id"])
        blockchain = state["blockchain"]
        
        sorted_messages = sort_messages(received_messages)
        prop_mess, vote_mess, echo_mess, recov_mess = sorted_messages
        
        send_messages_list = []
        for i in range (self.num_nodes):
            send_messages_list.append ([])
        if self.phase == 0:
            hash = hash_function ("epoch_" + str (self.epoch))
            
            # Not quite right
            if (hash % self.num_nodes == self.id):
                self.proposer = True
            else:
                self.proposer = False
            
            if (self.proposer):
                # get previous hash
                longest_blockchain_blocks = blockchain.most_depth_blocks()
                prev_hash = StreamletBlock.block_hash(longest_blockchain_blocks[0])
                # get transactions
                transactions = "STUB" #input()
                proposal = StreamletBlock.static_stringify(prev_hash, self.epoch, transactions)
                signature = create_signature ("key_" + str(self.id), proposal)
                m = Message (proposal, signature)
                #send_message = "proposal;" + self.id + ";" + proposal + ";" + signature
                np.send_messages (m)
                # send
                    
            self.phase = 1
            
        elif self.phase == 1:
            if (not self.proposer):
                for proposal in prop_mess:
                    accept_prop = True
                
                    contents = proposal.split(";")
                    prop_id = contents[1]
                    proposal = contents[2]
                    signature = contents[3]
                    
                    if (not verify_signature ("key_" + prop_id, proposal, signature)):
                        accept_prop = False
                    
                    prop_contents = proposal.split(",")
                    prev_hash = prop_contents[0]
                    epoch = prop_contents[1]
                    trans = prop_contents[2]
                    
                    if (not state["blockchain"].vote_for (prev_hash)):
                        accept_prop = False
                    
                    curr_leader = hash_function("epoch_" + str(epoch)) % self.num_nodes
                    if (curr_leader != prop_id):
                        accept_prop = False
                        
                    if (accept_prop):
                        vote()
                    
         
        # on receipt of 2/3 majority of votes, then notarize (should listen here for votes)
        
         
        # echo proposals
        
        # echo votes
        
        state["round"] = state["round"] + 1
        state["epoch"] = state["round"] % 3
        
