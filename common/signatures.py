SIG_FORMAT = "Sig:{}(Message:{})"


def create_signature(key, message):
    return SIG_FORMAT.format(key, message)


def verify_signature(key, message, tag):
    return SIG_FORMAT.format(key, message) == tag
