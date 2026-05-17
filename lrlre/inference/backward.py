"""
Simple backward chaining for Phase 2
"""

def backward_chain(goal: str, rules: dict, facts: list, depth: int = 0, max_depth: int = 5) -> bool:
    """
    Simple backward chaining algorithm

    Args:
        goal: Goal to prove (e.g., 'parent(john,steve)')
        rules: Dictionary of rules {premise: conclusion}
        facts: List of facts as tuples
        depth: Current recursion depth
        max_depth: Maximum recursion depth

    Returns:
        True if goal can be proved, False otherwise
    """
    if depth > max_depth:
        return False

    # Extract predicate from goal
    def extract_predicate(expr):
        if '(' in expr and ')' in expr:
            return expr.split('(')[0], expr.split('(')[1].split(')')[0].split(',')
        return expr, []

    goal_pred, goal_args = extract_predicate(goal)

    # Check if goal matches any fact directly
    for fact_tuple in facts:
        subject, obj, metadata = fact_tuple
        fact_pred = metadata.get('label', '')

        # Create fact expression
        fact_expr = f"{fact_pred}({subject},{obj})"
        fact_pred, fact_args = extract_predicate(fact_expr)

        # Check if predicates match and arguments match
        if goal_pred == fact_pred and goal_args == fact_args:
            return True

    # Try to prove using rules
    for premise, conclusion in rules.items():
        conc_pred, conc_args = extract_predicate(conclusion)

        # Check if conclusion matches goal
        if goal_pred == conc_pred:
            # Simple variable substitution (assume premise is single predicate)
            prem_pred, prem_args = extract_predicate(premise)

            # Try to prove premise
            if backward_chain(premise, rules, facts, depth + 1, max_depth):
                return True

    return False
