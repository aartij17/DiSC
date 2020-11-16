def create_signature(key, message):
    return "{}({})".format(key, message)


def verify_signature(key, message, tag):
    return "{}({})".format(key, message) == tag
