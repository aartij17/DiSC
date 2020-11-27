from protocols.dolev_strong import DolevStrong
from common.constants import *


def get_protocol(protocol, num_faulty_nodes, num_honest_nodes):
    if protocol == DOLEV_STRONG_PROTOCOL:
        return DolevStrong(num_faulty_nodes, num_honest_nodes)
    if protocol == STREAMLET_PROTOCOL:
        return  # TODO: Initialize Streamlet protocol
