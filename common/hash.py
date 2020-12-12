import random

random.seed(2)
hashfuncdict = {}


def hash_function(input):
    if (input in hashfuncdict):
        return hashfuncdict[input]
    else:
        val = random.randint(0, 100000000)
        hashfuncdict[input] = val
        return val
