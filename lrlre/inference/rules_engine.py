"""
RULES ENGINE - Enterprise Edition
Rule-based inference engine for the LRLRE system.
Provides forward and backward chaining capabilities.
"""
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
import time
import re


@dataclass
class Rule:
    """Represents an inference rule."""
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    action: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]]
    priority: int = 0
    description: str = ""


@dataclass
class Fact:
    """Represents a fact in the knowledge base."""
    predicate: str
    args: List[Any]
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)
    source: str = "user"


class RuleEngine:
    """
    Rule-based inference engine supporting forward and backward chaining.
    """
    
    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rules: List[Rule] = rules or []
        self.facts: List[Fact] = []
        self.inferred_facts: List[Fact] = []
        self._rule_history: List[Dict[str, Any]] = []
        
    def add_rule(self, name: str, condition: Callable, action: Callable, 
                 priority: int = 0, description: str = "") -> None:
        """Add a rule to the engine."""
        rule = Rule(
            name=name,
            condition=condition,
            action=action,
            priority=priority,
            description=description
        )
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        
    def add_fact(self, predicate: str, args: List[Any], confidence: float = 1.0,
                 source: str = "user") -> Fact:
        """Add a fact to the knowledge base."""
        fact = Fact(
            predicate=predicate,
            args=args,
            confidence=confidence,
            source=source
        )
        self.facts.append(fact)
        return fact
    
    def _match_fact(self, fact: Fact, pattern: Dict[str, Any]) -> bool:
        """Check if a fact matches a pattern."""
        if 'predicate' in pattern and pattern['predicate'] != fact.predicate:
            return False
        if 'args' in pattern:
            if len(pattern['args']) != len(fact.args):
                return False
            for i, arg_pattern in enumerate(pattern['args']):
                if arg_pattern is not None and arg_pattern != fact.args[i]:
                    return False
        return True
    
    def query(self, predicate: str, args: Optional[List[Any]] = None) -> List[Fact]:
        """Query facts matching the given predicate and optional args."""
        pattern = {'predicate': predicate}
        if args:
            pattern['args'] = args
        return [f for f in self.facts + self.inferred_facts if self._match_fact(f, pattern)]
    
    def forward_chain(self, max_iterations: int = 100) -> List[Fact]:
        """
        Perform forward chaining inference.
        Applies rules to facts to derive new conclusions.
        """
        start_time = time.time()
        new_facts = []
        iterations = 0
        
        while iterations < max_iterations:
            made_inference = False
            
            for rule in self.rules:
                all_facts = self.facts + self.inferred_facts
                
                for fact in all_facts:
                    try:
                        if rule.condition({'fact': fact, 'facts': all_facts}):
                            result = rule.action({'fact': fact, 'facts': all_facts})
                            
                            if result and isinstance(result, dict):
                                new_fact = Fact(
                                    predicate=result.get('predicate', ''),
                                    args=result.get('args', []),
                                    confidence=result.get('confidence', 0.5) * fact.confidence,
                                    source=f"inferred:{rule.name}"
                                )
                                
                                # Check if fact already exists
                                if not any(f.predicate == new_fact.predicate and 
                                          f.args == new_fact.args for f in self.inferred_facts):
                                    self.inferred_facts.append(new_fact)
                                    new_facts.append(new_fact)
                                    made_inference = True
                                    
                                    self._rule_history.append({
                                        'rule': rule.name,
                                        'triggered_by': fact.predicate,
                                        'result': new_fact.predicate,
                                        'iteration': iterations
                                    })
                    except Exception as e:
                        continue  # Skip rules that fail
            
            if not made_inference:
                break
            iterations += 1
        
        return new_facts
    
    def backward_chain(self, goal: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Perform backward chaining to prove a goal.
        Returns (success, proof_tree).
        """
        proof_tree = []
        
        def prove(subgoal: Dict[str, Any], depth: int = 0) -> bool:
            if depth > 50:  # Prevent infinite recursion
                return False
                
            # Check if goal is already satisfied by facts
            matching_facts = self.query(
                subgoal.get('predicate', ''),
                subgoal.get('args')
            )
            
            if matching_facts:
                proof_tree.append({
                    'type': 'fact',
                    'goal': subgoal,
                    'matched_by': [{'predicate': f.predicate, 'args': f.args} 
                                   for f in matching_facts]
                })
                return True
            
            # Try to prove using rules
            for rule in self.rules:
                try:
                    # Check if rule can potentially prove this goal
                    test_result = rule.action({'fact': None, 'facts': []})
                    if test_result and test_result.get('predicate') == subgoal.get('predicate'):
                        # Try to satisfy rule conditions
                        dummy_fact = Fact(predicate='dummy', args=[])
                        if rule.condition({'fact': dummy_fact, 'facts': self.facts}):
                            proof_tree.append({
                                'type': 'rule',
                                'goal': subgoal,
                                'rule': rule.name
                            })
                            return True
                except:
                    continue
            
            return False
        
        success = prove(goal)
        return success, proof_tree
    
    def get_all_facts(self) -> List[Dict[str, Any]]:
        """Get all facts (base and inferred) as dictionaries."""
        all_facts = self.facts + self.inferred_facts
        return [
            {
                'predicate': f.predicate,
                'args': f.args,
                'confidence': f.confidence,
                'source': f.source
            }
            for f in all_facts
        ]
    
    def infer(self, graph_facts: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Main inference method. Loads facts from graph and runs forward chaining.
        """
        start_time = time.time()
        
        # Load facts from graph if provided
        if graph_facts:
            for gf in graph_facts:
                predicate = gf.get('predicate', '')
                args = gf.get('args', [])
                if isinstance(args, list):
                    self.add_fact(predicate, args, gf.get('confidence', 1.0))
                else:
                    # Handle case where args might be a single value
                    self.add_fact(predicate, [args], gf.get('confidence', 1.0))
        
        # Run forward chaining
        new_facts = self.forward_chain()
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'inferences': [
                {
                    'predicate': f.predicate,
                    'args': f.args,
                    'confidence': f.confidence,
                    'source': f.source
                }
                for f in new_facts[:10]  # Return top 10
            ],
            'inference_count': len(new_facts),
            'total_facts': len(self.facts) + len(self.inferred_facts),
            'processing_time_ms': round(processing_time, 2),
            'rules_fired': len(self._rule_history)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            'base_facts': len(self.facts),
            'inferred_facts': len(self.inferred_facts),
            'total_facts': len(self.facts) + len(self.inferred_facts),
            'rules': len(self.rules),
            'rules_fired': len(self._rule_history)
        }
    
    def clear(self) -> None:
        """Clear all facts and history."""
        self.facts.clear()
        self.inferred_facts.clear()
        self._rule_history.clear()


# Default rules for common inference patterns
def create_default_rules() -> List[Rule]:
    """Create a set of default inference rules."""
    return [
        Rule(
            name='symmetric_relation',
            condition=lambda ctx: ctx['fact'].predicate in ['knows', 'married_to', 'sibling_of'],
            action=lambda ctx: {
                'predicate': ctx['fact'].predicate,
                'args': [ctx['fact'].args[1], ctx['fact'].args[0]] if len(ctx['fact'].args) >= 2 else [],
                'confidence': 0.95
            },
            priority=10,
            description='Symmetric relations work both ways'
        ),
        Rule(
            name='transitive_location',
            condition=lambda ctx: ctx['fact'].predicate == 'located_in',
            action=lambda ctx: {
                'predicate': 'located_in',
                'args': [ctx['fact'].args[0], 'unknown_region'],
                'confidence': 0.7
            },
            priority=5,
            description='Things located somewhere are also in a broader region'
        ),
        Rule(
            name='type_inheritance',
            condition=lambda ctx: ctx['fact'].predicate == 'is_a',
            action=lambda ctx: {
                'predicate': 'has_property',
                'args': [ctx['fact'].args[0], 'inherits_from_' + str(ctx['fact'].args[1])],
                'confidence': 0.8
            },
            priority=8,
            description='Type membership implies property inheritance'
        )
    ]


def test_rule_engine():
    """Test function for the rule engine."""
    print("=" * 60)
    print("RULE ENGINE TEST")
    print("=" * 60)
    
    engine = RuleEngine(create_default_rules())
    
    # Add some facts
    engine.add_fact('knows', ['Alice', 'Bob'], confidence=1.0)
    engine.add_fact('located_in', ['Paris', 'France'], confidence=0.95)
    engine.add_fact('is_a', ['Dog', 'Mammal'], confidence=1.0)
    
    # Run inference
    result = engine.infer()
    
    print(f"\nBase facts: {len(engine.facts)}")
    print(f"Inferred facts: {result['inference_count']}")
    print(f"Processing time: {result['processing_time_ms']}ms")
    
    print("\nInferred facts:")
    for inf in result['inferences'][:5]:
        print(f"  • {inf['predicate']}({', '.join(str(a) for a in inf['args'])}) "
              f"[conf: {inf['confidence']:.2f}]")
    
    print("\nEngine stats:", engine.get_stats())
    print("=" * 60)


if __name__ == "__main__":
    test_rule_engine()
