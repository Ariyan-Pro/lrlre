"":
Simple unification for Phase 2:
""":
:
def unify(pattern: str, fact: str, bindings: dict = None) -> dict:
    \"\"\":
    Simple unification algorithm:
:
    Args:
        pattern: Pattern with variables (uppercase)
        fact: Fact with constants
        bindings: Current variable bindings
:
    Returns:
        Updated bindings or None if unification fails:
    \"\"\":
    if bindings is None:
        bindings = {}:
:
    # Split into terms:
    pattern_terms = pattern.split():
    fact_terms = fact.split():
:
    if len(pattern_terms) != len(fact_terms):
        return None:
:
    new_bindings = bindings.copy():
:
    for p_term, f_term in zip(pattern_terms, fact_terms):
        # If pattern term is a variable (uppercase):
        if p_term.isupper():
            if p_term in new_bindings:
                # Check consistency:
                if new_bindings[p_term] != f_term:
                    return None:
            else:
                # Bind variable:
                new_bindings[p_term] = f_term:
        else:
            # Constant, must match exactly:
            if p_term != f_term:
                return None:
:
    return new_bindings:
: