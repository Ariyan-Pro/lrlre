"""
Simple backward chaining for Phase 2 - FIXED VERSION
Now includes proper variable unification for rule-based inference
"""
import re
from typing import Dict, List, Any, Tuple, Optional

def extract_predicate(expr: str) -> Tuple[str, List[str]]:
    """Extract predicate name and arguments from an expression."""
    if '(' in expr and ')' in expr:
        pred = expr.split('(')[0]
        args_str = expr.split('(')[1].split(')')[0]
        args = [arg.strip() for arg in args_str.split(',')]
        return pred, args
    return expr, []


def unify(goal_args: List[str], fact_args: List[str]) -> Optional[Dict[str, str]]:
    """
    Unify goal arguments with fact/rule arguments.
    Returns a substitution dictionary if unification succeeds, None otherwise.
    
    Variables (uppercase or starting with X, Y, Z) can match any term.
    This function handles variables in EITHER argument list.
    """
    if len(goal_args) != len(fact_args):
        return None
    
    substitutions = {}
    
    for goal_arg, fact_arg in zip(goal_args, fact_args):
        goal_arg = goal_arg.strip()
        fact_arg = fact_arg.strip()
        
        # Check if either argument is a variable (uppercase or starts with X/Y/Z)
        goal_is_var = (goal_arg[0].isupper() if goal_arg else False)
        fact_is_var = (fact_arg[0].isupper() if fact_arg else False)
        
        if goal_is_var and fact_is_var:
            # Both are variables - they can match but don't bind yet
            continue
        elif goal_is_var:
            # Goal is variable, bind it to fact value
            if goal_arg in substitutions:
                # Variable already bound, check consistency
                if substitutions[goal_arg] != fact_arg:
                    return None
            else:
                substitutions[goal_arg] = fact_arg
        elif fact_is_var:
            # Fact/rule is variable, bind it to goal value
            if fact_arg in substitutions:
                # Variable already bound, check consistency
                if substitutions[fact_arg] != goal_arg:
                    return None
            else:
                substitutions[fact_arg] = goal_arg
        elif goal_arg == fact_arg:
            # Constants must match exactly
            continue
        else:
            # Mismatch between different constants
            return None
    
    return substitutions


def apply_substitution(expr: str, substitutions: Dict[str, str]) -> str:
    """Apply variable substitutions to an expression."""
    result = expr
    for var, value in substitutions.items():
        # Replace variable with its bound value
        result = re.sub(r'\b' + re.escape(var) + r'\b', value, result)
    return result


def backward_chain(goal: str, rules: dict, facts: list, depth: int = 0, 
                   max_depth: int = 5, substitutions: Optional[Dict[str, str]] = None) -> bool:
    """
    Backward chaining algorithm with proper variable unification.
    
    Args:
        goal: Goal to prove (e.g., 'mortal(socrates,human)')
        rules: Dictionary of rules {premise: conclusion}
        facts: List of facts as tuples (subject, object, metadata)
        depth: Current recursion depth
        max_depth: Maximum recursion depth
        substitutions: Current variable bindings
    
    Returns:
        True if goal can be proved, False otherwise
    """
    if substitutions is None:
        substitutions = {}
    
    if depth > max_depth:
        return False
    
    goal_pred, goal_args = extract_predicate(goal)
    
    # Check if goal matches any fact directly (with unification)
    for fact_tuple in facts:
        subject, obj, metadata = fact_tuple
        fact_pred = metadata.get('label', '')
        
        # Create fact expression
        fact_expr = f"{fact_pred}({subject},{obj})"
        _, fact_args = extract_predicate(fact_expr)
        
        # Try to unify goal with fact
        if goal_pred == fact_pred:
            unified = unify(goal_args, fact_args)
            if unified is not None:
                # Merge with existing substitutions
                new_subs = {**substitutions, **unified}
                
                # If goal has no unbound variables, we've proven it
                goal_has_vars = any(
                    (arg.strip()[0].isupper() if arg.strip() else False)
                    for arg in goal_args
                )
                
                if not goal_has_vars or all(
                    var in new_subs for arg in goal_args 
                    for var in [arg.strip()] 
                    if (arg.strip()[0].isupper() if arg.strip() else False)
                ):
                    return True
    
    # Try to prove using rules (backward chaining through premises)
    for premise, conclusion in rules.items():
        conc_pred, conc_args = extract_predicate(conclusion)
        
        # Check if conclusion can unify with goal
        if goal_pred == conc_pred:
            unified = unify(goal_args, conc_args)
            if unified is not None:
                # Apply substitution to premise
                new_subs = {**substitutions, **unified}
                instantiated_premise = apply_substitution(premise, new_subs)
                
                # Recursively try to prove the premise
                if backward_chain(instantiated_premise, rules, facts, depth + 1, 
                                 max_depth, new_subs):
                    return True
    
    return False
