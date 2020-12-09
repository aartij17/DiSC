
import sys

from main import log
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
        for m in received_messages:
            contents = m.content.split("`")
            if contents[0] == "proposal":
                proposal_messages.append (m)
            elif contents[0] == "vote":
                vote_messages.append (m)
            #elif contents[0] == "echo":
            #    for echo
            #    echo_messages[i].append (message)
        
        return (proposal_messages, vote_messages, echo_messages)
        
        
    
    def run_protocol_one_round(self, state, np, l=None):
        
        log.info("################################### ROUND: {}, NODE_ID: {} ###################################".format(state["round"], state["node_id"]))
    
        log.debug("Epoch = " + str (state["epoch"] ))
        log.debug("Phase = " + str (state["phase"] ))
    
        log.debug ("Proposer = " + str(hash_function ("epoch_" + str (state["epoch"]))% self.num_nodes))

        received_messages = np.receive_messages(state["node_id"])
        # 1-D array?
        
        #print (received_messages)
        state["received_messages"] = received_messages
        blockchain = state["blockchain"]
        
        
        sorted_messages = self.sort_messages(received_messages)
        #print (sorted_messages)
        prop_mess, vote_mess, echo_mess = sorted_messages
        
        if state["phase"] == 0: # proposal phase
            hash = hash_function ("epoch_" + str (state["epoch"]))

            #log.debug ("hash%num_nodes " + str(hash % self.num_nodes))
            #log.debug ("state[node_id] " + str(state["node_id"]))
            if (hash % self.num_nodes == state["node_id"]):
                state["proposer"] = True
            else:
                state["proposer"] = False
            
            if (state["proposer"]):
                # get previous hash
                longest_blockchain_blocks = blockchain.most_depth_blocks()
                prev_hash = StreamletBlock.block_hash(longest_blockchain_blocks[0])
                # get transactions
                transactions = "Trans_" + str (state["round"]) #input()
                proposal = StreamletBlock.static_stringify(prev_hash, state["epoch"], transactions)
                signature = create_signature ("key_" + str(state["node_id"]), proposal)
                m = Message ("proposal`" + proposal, state["node_id"], self.round, [signature])
                np.broadcast(m, False)
                
                state["proposals"][proposal] = False
                #state["vote"][proposal] = 1
            
        elif state["phase"] == 1: # receiving and voting for proposal phase
            self.handle_proposals (prop_mess, state, np)
                    
         
        # on receipt of 2/3 majority of votes, then notarize (should listen here for votes)
        elif state["phase"] == 2: # receiving votes and notarizing on the blockchain
            self.handle_votes (vote_mess, state)

        # echo proposals
        # cut corners
        # echo votes
        
        state["blockchain"].print_blockchain()
        
        
        state["round"] = state["round"] + 1
        state["epoch"] = int(state["round"] / 3)
        state["phase"] = state["round"] % 3
        
        
    def vote(self, state, np, proposal):
        # broadcast vote to everyone
        # add vote to own counter
        prop_contents = proposal.split(",")
        prev_hash = prop_contents[0]
        epoch = prop_contents[1]
        trans = prop_contents[2]
        prop_str = StreamletBlock.static_stringify(prev_hash, epoch, trans)
        
        log.debug("Proposal received -> " + prop_str)
        
        signature = create_signature ("key_" + str(state["node_id"]), prop_str)
        
        m = Message("vote`" + proposal, state["node_id"], self.round, [signature])
        
        # broadcast message
        np.broadcast(m, False)
        
                
        state["proposals"][proposal] = False
        

    def handle_votes (self, vote_mess, state):
        for vot in vote_mess:
            messages = Message.get_message_content(vot).split("`")
            proposal = messages[1]
            voter = vot.get_sender()
            
            prop_contents = proposal.split(",")
            prev_hash = int(prop_contents[0])
            epoch = int(prop_contents[1])
            trans = prop_contents[2]
            
            if (verify_signature("key_" + str(voter), proposal, Message.get_message_signatures(vot)[0])):
                if not proposal in state["proposals"]:
                    state["proposals"][proposal] = False
                if not proposal in state["vote"]:
                    #print ("Incrementing")
                    state["vote"][proposal] = 1
                else:
                    #print ("Incrementing")
                    state["vote"][proposal] += 1
               
               
                #print ("Num votes = " + str (state["vote"][proposal]))
                #print ("Condition = " + str(int(2 * (self.num_faulty_nodes + self.num_honest_nodes) / 3) + 1))
                if (state["vote"][proposal] >= int(2 * (self.num_faulty_nodes + self.num_honest_nodes) / 3) + 1 and not state["proposals"][proposal]):
                    state["proposals"][proposal] = True
                    state["blockchain"].append_to_blockchain (prev_hash, epoch, trans)
                    
            
            

    def handle_proposals (self, prop_mess, state, np):
        for prop in prop_mess:
            # add to proposal state
            accept_prop = True

            prop_id = prop.get_sender()
            proposal = prop.content.split("`")[1]
            signature = prop.get_message_signatures()[0]
            
            state["proposals"][proposal] = False
            
            #print ("Accept proposal 1 " + str (accept_prop))
            
            if (not verify_signature ("key_" + str(prop_id), proposal, signature)):
                accept_prop = False
            
            prop_contents = proposal.split(",")
            prev_hash = int(prop_contents[0])
            epoch = int(prop_contents[1])
            trans = prop_contents[2]
            
            #print ("Accept proposal 2 " + str (accept_prop))
            
            if (not state["blockchain"].vote_for (prev_hash)):
                accept_prop = False
            
            #print ("Accept proposal 3 " + str (accept_prop))
                
            curr_leader = hash_function("epoch_" + str(epoch)) % self.num_nodes
            
            if (curr_leader != int(prop_id)):
                accept_prop = False
                
                
            log.debug ("Accept proposal 4 " + str (accept_prop))
            #print ("Accept proposal 4 " + str (accept_prop))
            if (accept_prop):
                self.vote(state, np, proposal)
