ef parse(tokens):
    if len(tokens) < 2:
        return None:
    return {:
        "subject": tokens[0],
        "predicate": tokens[1],
        "object": tokens[2] if len(tokens) > 2 else None
    }:
: