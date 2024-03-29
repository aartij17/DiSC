from protocols.adversaries.do_nothing_protocol import *
from protocols.adversaries.dolev_strong_adversary import *
from protocols.adversaries.random_broadcast_protocol import *
from protocols.dolev_strong import DolevStrong
from protocols.dolev_strong_weak import DolevStrongWeak
from protocols.streamlet import Streamlet


def get_protocol(protocol, num_faulty_nodes, num_honest_nodes):
    if protocol == DOLEV_STRONG_PROTOCOL:
        return DolevStrong(num_faulty_nodes, num_honest_nodes)
    if protocol == DOLEV_STRONG_WEAK_PROTOCOL:
        return DolevStrongWeak(num_faulty_nodes, num_honest_nodes)
    elif protocol == STREAMLET_PROTOCOL:
        return Streamlet(num_faulty_nodes, num_honest_nodes)
    elif protocol == ADVERSARY_DONOTHING_PROTOCOL:
        return DoNothingAdversary(num_faulty_nodes, num_honest_nodes)
    elif protocol == ADVERSARY_RANDOMBROADCAST_PROTOCOL:
        return RandomBroadcastAdversary(num_faulty_nodes, num_honest_nodes)
    elif protocol == DOLEV_STRONG_ADVERSARY:
        return DolevStrongAdversary(num_faulty_nodes, num_honest_nodes)
