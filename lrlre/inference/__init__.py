"""Inference module for LRLRE - Forward and backward chaining, pattern matching, and unification"""

from .forward import forward_chain, create_fact_from_conclusion
from .backward import backward_chain
from .unification import unify
from .pattern_engine import PatternEngine

__all__ = [
    'forward_chain',
    'create_fact_from_conclusion',
    'backward_chain',
    'unify',
    'PatternEngine',
]
