"""
Simple forward chaining for Phase 2
"""

def forward_chain(rules: dict, facts: list) -> list:
    """
    Simple forward chaining algorithm

    Args:
        rules: Dictionary of rules {premise: conclusion}
        facts: List of facts as tuples

    Returns:
        List of new inferred facts
    """
    new_inferences = []

    for premise, conclusion in rules.items():
        # Check if premise is satisfied by facts
        prem_satisfied = False

        # Extract predicate from premise
        if '(' in premise and ')' in premise:
            prem_pred = premise.split('(')[0]
            prem_args = premise.split('(')[1].split(')')[0].split(',')

            # Check each fact
            for fact_tuple in facts:
                subject, obj, metadata = fact_tuple
                fact_pred = metadata.get('label', '')

                if prem_pred == fact_pred:
                    # Simple matching - for Phase 2, just check predicate
                    prem_satisfied = True
                    break

        if prem_satisfied:
            # Apply rule - for Phase 2, use conclusion as is
            new_inferences.append(create_fact_from_conclusion(conclusion))

    return new_inferences


def create_fact_from_conclusion(conclusion: str):
    """Create fact tuple from conclusion string"""
    if '(' in conclusion and ')' in conclusion:
        pred = conclusion.split('(')[0]
        args = conclusion.split('(')[1].split(')')[0].split(',')
        if len(args) >= 2:
            return (args[0], args[1], {'label': pred, 'confidence': 0.7})

    # Fallback
    return (conclusion, '', {'label': 'inferred'})
