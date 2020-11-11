from Protocols.dolev_strong import DolevStrong
from common.constants import *


def get_protocol(protocol):
    if protocol == DOLEV_STRONG_PROTOCOL:
        return DolevStrong()
