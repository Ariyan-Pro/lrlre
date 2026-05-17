"""
Simple unification for Phase 2
"""

def unify(pattern: str, fact: str, bindings: dict = None) -> dict:
    """
    Simple unification algorithm

    Args:
        pattern: Pattern with variables (single uppercase letters like X, Y, Z)
                 First term is typically a predicate (constant)
        fact: Fact with constants
        bindings: Current variable bindings

    Returns:
        Updated bindings or None if unification fails
    """
    if bindings is None:
        bindings = {}

    # Split into terms
    pattern_terms = pattern.split()
    fact_terms = fact.split()

    if len(pattern_terms) != len(fact_terms):
        return None

    new_bindings = bindings.copy()

    for i, (p_term, f_term) in enumerate(zip(pattern_terms, fact_terms)):
        # First term is always a predicate (constant) - must match exactly
        if i == 0:
            if p_term != f_term:
                return None
        # Single uppercase letters (X, Y, Z, etc.) are variables
        elif len(p_term) == 1 and p_term.isupper():
            if p_term in new_bindings:
                # Check consistency
                if new_bindings[p_term] != f_term:
                    return None
            else:
                # Bind variable
                new_bindings[p_term] = f_term
        else:
            # Constant, must match exactly
            if p_term != f_term:
                return None

    return new_bindings
