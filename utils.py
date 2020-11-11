from dolev_strong import DolevStrong
from constants import *


def get_protocol(protocol):
    if protocol == DOLEV_STRONG_PROTOCOL:
        return DolevStrong()
