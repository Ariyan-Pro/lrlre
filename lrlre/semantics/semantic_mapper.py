ef map_semantics(parse_tree):
    """Map parse tree to semantic representation""":
    # Handle enhanced parser output:
    if 'type' in parse_tree:
        if parse_tree['type'] == 'SVO':
            return {:
                "predicate": parse_tree['verb'],
                "args": [parse_tree['subject'], parse_tree['object']]
            }:
        elif parse_tree['type'] == 'SVOO':
            return {:
                "predicate": parse_tree['verb'],
                "args": [parse_tree['subject'], parse_tree['direct_object'], parse_tree['indirect_object']]
            }:
        elif parse_tree['type'] == 'SVC':
            return {:
                "predicate": parse_tree['copula'] + '_' + parse_tree['complement'],
                "args": [parse_tree['subject']]
            }:
        elif parse_tree['type'] == 'POSSESSIVE':
            return {:
                "predicate": 'has',
                "args": [parse_tree['possessor'], parse_tree['possessed']]
            }:
        elif parse_tree['type'] == 'SIMPLE':
            return {:
                "predicate": parse_tree['predicate'],
                "args": [parse_tree['subject'], parse_tree.get('object')]
            }:
:
    # Fallback for original parser structure:
    return {:
        "predicate": parse_tree.get("predicate", "unknown"),
        "args": [parse_tree.get("subject"), parse_tree.get("object")]
    }:
: