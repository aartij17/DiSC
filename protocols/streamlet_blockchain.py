
from common.constants import *
from common.hash import hash_function

STREAMLETBLOCKDELIMITER = ","

class StreamletBlockchain:

    #TODO to string



    def __init__(self):
        self.blockchain_top = []
        self.blockchain_all = []
        self.finalized = []
        initialblock = StreamletBlock.create_initial()
        self.blockchain_top.append (initialblock)
        self.blockchain_all.append (initialblock)

    def append_to_blockchain (self, prev_hash, epoch_num, transactions):
        for block in self.blockchain_all:
            if (prev_hash == StreamletBlock.block_hash(block)):
                b = StreamletBlock (block, prev_hash, epoch_num, transactions)
                if (block in self.blockchain_top):
                    self.blockchain_top.remove (block)
                self.blockchain_top.append (b)
                self.blockchain_all.append (b)

        self.finalize()


    def finalize (self):
        found_three_in_a_row = None #middle block in three in a row
        for blocks in self.blockchain_top:
            curr_block = blocks
            consecutive = False
            print ("CURR_BLOCK")
            print (curr_block)
            while curr_block is not None and not curr_block.is_initial() and not curr_block in self.finalized:
                # If the previous block was consecutive and this is consecutive,
                # Then it must be three in a row and therefore finalized
                if (consecutive and curr_block.consecutive_epochs()):
                    found_three_in_a_row = curr_block
                    print ("Found Three is a row!!!! +_+_+_+_+_+_+_+_+_+_+_+_+_+_+")
                    break

                consecutive = curr_block.consecutive_epochs()

                curr_block = curr_block.get_prev_block()

            if (found_three_in_a_row != None):
                break

        if (found_three_in_a_row):
            # Adds everything from middle and before to the finalized blockchain
            curr_block = found_three_in_a_row
            while not curr_block in self.finalized:
                self.finalized.append (curr_block)
                curr_block = curr_block.get_prev_block()

            # Removes everything that would be inconsistent
            self.blockchain_top = [x for x in self.blockchain_top if x.leads_to_block(found_three_in_a_row) or x in finalized]
            self.blockchain_all = [x for x in self.blockchain_all if x.leads_to_block(found_three_in_a_row) or x in finalized]

    def vote_for (self, prev_hash):
        """
        largest_depth = 0
        hash_match_depth = 0
        for block in self.blockchain_top:
            depth = block.depth()
            if (depth > largest_depth):
                largest_depth = depth

            if (prev_hash == StreamletBlock.block_hash(block)):
                hash_match_depth = depth
        # vote for block if new block has longest depth and there is a match
        return hash_match_depth == largest_depth and largest_depth > 0
        """
        longest = self.most_depth_blocks()
        for block in longest:
            if (int(prev_hash) == StreamletBlock.block_hash(block)):
                return True
        return False


    def most_depth_blocks (self):
        largest_depth = 0
        for block in self.blockchain_top:
            depth = block.depth()
            if (depth > largest_depth):
                largest_depth = depth

        block_list = []
        for block in self.blockchain_top:
            depth = block.depth()
            if (depth == largest_depth):
                block_list.append (block)
        return block_list

class StreamletBlock:

    #TODO to string

    def __init__(self, prev_block, prev_hash, epoch_num, transactions):
        self.prev_block = prev_block
        self.prev_hash = prev_hash
        self.epoch_num = epoch_num
        self.transactions = transactions

    def consecutive_epochs (self):
        return (self.prev_block != None) and (self.epoch_num - 1 == self.prev_block.get_epoch_num())

    def get_prev_block (self):
        return self.prev_block

    def get_prev_hash (self):
        return self.prev_hash

    def get_epoch_num (self):
        return self.epoch_num

    def get_transactions(self):
        return transactions

    def is_initial (self):
        return self.epoch_num == -1

    def __eq__(self, other):
        return self.prev_block == other.get_prev_block() and self.epoch_num == other.get_epoch_num() and self.transactions == other.get_transactions()

    def leads_to_block (self, block):
        curr_block = self.prev_block
        while (not curr_block.is_initial()):
            if (curr_block == block):
                return True
            curr_block = curr_block.get_prev_block()
        return False

    def stringify(self):
        return "{}{}{}{}{}".format(
            self.prev_hash,
            STREAMLETBLOCKDELIMITER,
            self.epoch_num,
            STREAMLETBLOCKDELIMITER,
            self.transactions
        )

    def depth(self):
        if self.epoch_num < 0:
            return 1
        else:
            return self.prev_block.depth()

    @staticmethod
    def block_hash(block):
        return hash_function(block.stringify())

    @classmethod
    def create_initial(cls):
        return cls(None, "null", -2, "None")

    @staticmethod
    def static_destringify(string):
        split = string.split(STREAMLETBLOCKDELIMITER)
        return (int(split[0]), int(split[1]), split[2]) # (prev_hash, epoch_num, transactions)

    @staticmethod
    def static_stringify (prev_hash, epoch_num, transactions):
        return "{}{}{}{}{}".format(
            prev_hash,
            STREAMLETBLOCKDELIMITER,
            epoch_num,
            STREAMLETBLOCKDELIMITER,
            transactions
        )
