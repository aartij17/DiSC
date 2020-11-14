


def create_signature (key, message):
    return key + "(" + message + ")"

def verify_signature (key, message, tag):
    return ((key + "(" + message + ")") == tag)
