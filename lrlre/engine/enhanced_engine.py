"""
ENHANCED ENGINE - Advanced Reasoning Module
Provides enhanced inference capabilities with multi-strategy reasoning,
confidence propagation, and conflict resolution.
"""
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import time
import heapq


class InferenceStrategy(Enum):
    """Available inference strategies."""
    FORWARD = "forward"
    BACKWARD = "backward"
    MIXED = "mixed"
    BEST_FIRST = "best_first"


@dataclass(order=True)
class WeightedFact:
    """A fact with a weight for priority queue ordering."""
    weight: float
    fact: Dict[str, Any] = field(compare=False)


@dataclass
class InferenceResult:
    """Result of an inference operation."""
    conclusions: List[Dict[str, Any]]
    strategy_used: str
    confidence: float
    processing_time_ms: float
    steps_taken: int
    conflicts_resolved: int = 0


class EnhancedEngine:
    """
    Advanced reasoning engine with multiple inference strategies,
    confidence propagation, and conflict resolution.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.facts: List[Dict[str, Any]] = []
        self.rules: List[Dict[str, Any]] = []
        self.inference_history: List[Dict[str, Any]] = []
        self.confidence_threshold = self.config.get('confidence_threshold', 0.3)
        self.max_iterations = self.config.get('max_iterations', 100)
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Initialize default enhanced rules."""
        self.rules = [
            {
                'name': 'modus_ponens',
                'pattern': {'type': 'implication'},
                'apply': self._apply_modus_ponens,
                'weight': 1.0
            },
            {
                'name': 'transitive_reasoning',
                'pattern': {'type': 'relation_chain'},
                'apply': self._apply_transitive,
                'weight': 0.9
            },
            {
                'name': 'analogy',
                'pattern': {'type': 'similarity'},
                'apply': self._apply_analogy,
                'weight': 0.7
            },
            {
                'name': 'default_assumption',
                'pattern': {'type': 'default'},
                'apply': self._apply_default,
                'weight': 0.5
            }
        ]
    
    def _apply_modus_ponens(self, fact: Dict[str, Any], 
                            context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply modus ponens inference rule."""
        if fact.get('type') == 'implication' and fact.get('antecedent'):
            antecedent = fact['antecedent']
            consequent = fact.get('consequent', {})
            
            # Check if antecedent is satisfied
            for f in context.get('facts', []):
                if self._facts_match(f, antecedent):
                    return {
                        **consequent,
                        'confidence': fact.get('confidence', 1.0) * f.get('confidence', 1.0),
                        'derived_from': 'modus_ponens'
                    }
        return None
    
    def _apply_transitive(self, fact: Dict[str, Any],
                          context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply transitive reasoning."""
        transitive_predicates = ['greater_than', 'less_than', 'ancestor_of', 
                                  'part_of', 'located_in']
        
        if fact.get('predicate') in transitive_predicates:
            pred = fact['predicate']
            args = fact.get('args', [])
            
            if len(args) >= 2:
                # Look for chain: A->B and B->C implies A->C
                for other in context.get('facts', []):
                    if (other.get('predicate') == pred and 
                        len(other.get('args', [])) >= 2 and
                        other['args'][0] == args[1]):
                        return {
                            'predicate': pred,
                            'args': [args[0], other['args'][1]],
                            'confidence': min(fact.get('confidence', 1.0), 
                                            other.get('confidence', 1.0)) * 0.9,
                            'derived_from': 'transitive'
                        }
        return None
    
    def _apply_analogy(self, fact: Dict[str, Any],
                       context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply analogical reasoning."""
        # Simple analogy: if A is like B, and B has property P, then A might have P
        if fact.get('predicate') == 'similar_to':
            args = fact.get('args', [])
            if len(args) >= 2:
                source, target = args[0], args[1]
                
                # Find properties of source
                for f in context.get('facts', []):
                    if (f.get('args') and len(f['args']) >= 1 and 
                        f['args'][0] == source and 
                        f.get('predicate') not in ['similar_to', 'equals']):
                        return {
                            'predicate': f['predicate'],
                            'args': [target] + f['args'][1:],
                            'confidence': fact.get('confidence', 0.5) * f.get('confidence', 1.0) * 0.6,
                            'derived_from': 'analogy'
                        }
        return None
    
    def _apply_default(self, fact: Dict[str, Any],
                       context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply default assumptions."""
        defaults = {
            'bird': {'predicate': 'can_do', 'args': ['fly'], 'confidence': 0.8},
            'fish': {'predicate': 'can_do', 'args': ['swim'], 'confidence': 0.9},
            'mammal': {'predicate': 'has_property', 'args': ['warm_blooded'], 'confidence': 0.95}
        }
        
        if fact.get('predicate') == 'is_a' and len(fact.get('args', [])) >= 2:
            entity_type = str(fact['args'][1]).lower()
            if entity_type in defaults:
                default = defaults[entity_type]
                return {
                    **default,
                    'args': [fact['args'][0]] + default['args'],
                    'confidence': default['confidence'] * 0.7,
                    'derived_from': 'default'
                }
        return None
    
    def _facts_match(self, fact: Dict[str, Any], pattern: Dict[str, Any]) -> bool:
        """Check if a fact matches a pattern."""
        for key, value in pattern.items():
            if key == 'args' and isinstance(value, list):
                fact_args = fact.get('args', [])
                if len(value) != len(fact_args):
                    return False
                for i, v in enumerate(value):
                    if v is not None and v != fact_args[i]:
                        return False
            elif fact.get(key) != value:
                return False
        return True
    
    def add_fact(self, predicate: str = None, args: List[Any] = None,
                 confidence: float = 1.0, fact_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a fact to the knowledge base."""
        if fact_dict:
            fact = fact_dict.copy()
        else:
            fact = {
                'predicate': predicate,
                'args': args or [],
                'confidence': confidence,
                'timestamp': time.time()
            }
        
        # Check for conflicts
        conflicts = self._detect_conflicts(fact)
        if conflicts:
            self._resolve_conflicts(fact, conflicts)
        
        self.facts.append(fact)
        return fact
    
    def _detect_conflicts(self, new_fact: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect facts that conflict with the new fact."""
        conflicts = []
        for existing in self.facts:
            if (existing.get('predicate') == new_fact.get('predicate') and
                existing.get('args') == new_fact.get('args')):
                # Same fact with different confidence
                if abs(existing.get('confidence', 1.0) - new_fact.get('confidence', 1.0)) > 0.3:
                    conflicts.append(existing)
            # Contradictory predicates
            elif self._are_contradictory(existing, new_fact):
                conflicts.append(existing)
        return conflicts
    
    def _are_contradictory(self, fact1: Dict[str, Any], fact2: Dict[str, Any]) -> bool:
        """Check if two facts are contradictory."""
        contradictions = {
            ('is_a', 'is_not_a'),
            ('equals', 'not_equals'),
            ('greater_than', 'less_than'),
            ('true', 'false')
        }
        p1, p2 = fact1.get('predicate', ''), fact2.get('predicate', '')
        return (p1, p2) in contradictions or (p2, p1) in contradictions
    
    def _resolve_conflicts(self, new_fact: Dict[str, Any], 
                           conflicts: List[Dict[str, Any]]) -> None:
        """Resolve conflicts using confidence-based arbitration."""
        new_conf = new_fact.get('confidence', 0.5)
        
        for conflict in conflicts:
            old_conf = conflict.get('confidence', 0.5)
            if new_conf > old_conf:
                # Remove lower confidence fact
                self.facts.remove(conflict)
                new_fact['conflicts_resolved'] = new_fact.get('conflicts_resolved', 0) + 1
    
    def add_rule(self, name: str, pattern: Dict[str, Any], 
                 apply_func: callable, weight: float = 1.0) -> None:
        """Add a custom rule to the engine."""
        self.rules.append({
            'name': name,
            'pattern': pattern,
            'apply': apply_func,
            'weight': weight
        })
    
    def infer(self, strategy: InferenceStrategy = InferenceStrategy.FORWARD,
              goal: Optional[Dict[str, Any]] = None) -> InferenceResult:
        """
        Perform inference using the specified strategy.
        """
        start_time = time.time()
        steps = 0
        conflicts_resolved = 0
        
        if strategy == InferenceStrategy.FORWARD:
            conclusions, steps, conflicts = self._forward_chain()
        elif strategy == InferenceStrategy.BACKWARD:
            conclusions, steps, conflicts = self._backward_chain(goal or {})
        elif strategy == InferenceStrategy.MIXED:
            conclusions, steps, conflicts = self._mixed_strategy(goal)
        elif strategy == InferenceStrategy.BEST_FIRST:
            conclusions, steps, conflicts = self._best_first_search(goal)
        else:
            conclusions, steps, conflicts = self._forward_chain()
        
        processing_time = (time.time() - start_time) * 1000
        
        # Calculate overall confidence
        avg_confidence = (sum(c.get('confidence', 0.5) for c in conclusions) / 
                         len(conclusions)) if conclusions else 0.0
        
        result = InferenceResult(
            conclusions=conclusions[:20],  # Limit results
            strategy_used=strategy.value,
            confidence=round(avg_confidence, 3),
            processing_time_ms=round(processing_time, 2),
            steps_taken=steps,
            conflicts_resolved=conflicts
        )
        
        self.inference_history.append({
            'timestamp': time.time(),
            'strategy': strategy.value,
            'results_count': len(conclusions),
            'processing_time': processing_time
        })
        
        return result
    
    def _forward_chain(self) -> Tuple[List[Dict[str, Any]], int, int]:
        """Forward chaining inference."""
        conclusions = []
        steps = 0
        conflicts = 0
        iterations = 0
        
        while iterations < self.max_iterations:
            made_progress = False
            
            for rule in sorted(self.rules, key=lambda r: r['weight'], reverse=True):
                for fact in self.facts[-50:]:  # Recent facts
                    try:
                        result = rule['apply'](fact, {'facts': self.facts})
                        if result and result.get('confidence', 0) >= self.confidence_threshold:
                            # Check if conclusion is new
                            if not any(self._facts_match(result, c) for c in conclusions):
                                conclusions.append(result)
                                self.facts.append(result)
                                made_progress = True
                                steps += 1
                                if 'conflicts_resolved' in result:
                                    conflicts += result['conflicts_resolved']
                    except Exception:
                        continue
            
            if not made_progress:
                break
            iterations += 1
        
        return conclusions, steps, conflicts
    
    def _backward_chain(self, goal: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], int, int]:
        """Backward chaining from a goal."""
        conclusions = []
        steps = 0
        conflicts = 0
        
        def prove(subgoal: Dict[str, Any], depth: int = 0) -> List[Dict[str, Any]]:
            nonlocal steps, conflicts
            if depth > 30:
                return []
            
            steps += 1
            
            # Check existing facts
            for fact in self.facts:
                if self._facts_match(fact, subgoal):
                    return [fact]
            
            # Try rules
            for rule in self.rules:
                try:
                    for fact in self.facts:
                        result = rule['apply'](fact, {'facts': self.facts})
                        if result and self._facts_match(result, subgoal):
                            return [result]
                except:
                    continue
            
            return []
        
        if goal:
            conclusions = prove(goal)
        
        return conclusions, steps, conflicts
    
    def _mixed_strategy(self, goal: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], int, int]:
        """Mixed forward and backward strategy."""
        # Start with some forward chaining
        fwd_conclusions, fwd_steps, fwd_conflicts = self._forward_chain()
        
        # Then use backward chaining if goal provided
        if goal:
            bwd_conclusions, bwd_steps, bwd_conflicts = self._backward_chain(goal)
            return (fwd_conclusions + bwd_conclusions, 
                    fwd_steps + bwd_steps, 
                    fwd_conflicts + bwd_conflicts)
        
        return fwd_conclusions, fwd_steps, fwd_conflicts
    
    def _best_first_search(self, goal: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], int, int]:
        """Best-first search using confidence as heuristic."""
        conclusions = []
        steps = 0
        conflicts = 0
        
        # Priority queue: (-confidence, fact)
        pq = []
        for fact in self.facts:
            heapq.heappush(pq, WeightedFact(-fact.get('confidence', 0.5), fact))
        
        visited: Set[str] = set()
        iterations = 0
        
        while pq and iterations < self.max_iterations:
            weighted = heapq.heappop(pq)
            fact = weighted.fact
            
            # Create unique key for fact
            fact_key = f"{fact.get('predicate')}_{str(fact.get('args'))}"
            if fact_key in visited:
                continue
            visited.add(fact_key)
            
            steps += 1
            
            # Apply rules
            for rule in self.rules:
                try:
                    result = rule['apply'](fact, {'facts': self.facts})
                    if result and result.get('confidence', 0) >= self.confidence_threshold:
                        result_key = f"{result.get('predicate')}_{str(result.get('args'))}"
                        if result_key not in visited:
                            conclusions.append(result)
                            heapq.heappush(pq, WeightedFact(-result.get('confidence', 0.5), result))
                            
                            if 'conflicts_resolved' in result:
                                conflicts += result['conflicts_resolved']
                except:
                    continue
            
            iterations += 1
        
        return conclusions, steps, conflicts
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            'total_facts': len(self.facts),
            'rules_count': len(self.rules),
            'inferences_run': len(self.inference_history),
            'avg_confidence': sum(f.get('confidence', 0.5) for f in self.facts) / len(self.facts) if self.facts else 0,
            'config': self.config
        }
    
    def clear(self) -> None:
        """Clear all facts and history."""
        self.facts.clear()
        self.inference_history.clear()


def test_enhanced_engine():
    """Test function for the enhanced engine."""
    print("=" * 60)
    print("ENHANCED ENGINE TEST")
    print("=" * 60)
    
    engine = EnhancedEngine({'confidence_threshold': 0.4})
    
    # Add facts
    engine.add_fact('is_a', ['Tweety', 'bird'], confidence=0.95)
    engine.add_fact('greater_than', [5, 3], confidence=1.0)
    engine.add_fact('greater_than', [3, 1], confidence=1.0)
    engine.add_fact('similar_to', ['cat', 'dog'], confidence=0.7)
    engine.add_fact('can_do', ['cat', 'meow'], confidence=0.9)
    
    # Test forward chaining
    print("\n--- Forward Chaining ---")
    result = engine.infer(InferenceStrategy.FORWARD)
    print(f"Strategy: {result.strategy_used}")
    print(f"Conclusions: {len(result.conclusions)}")
    print(f"Avg confidence: {result.confidence}")
    print(f"Steps: {result.steps_taken}")
    
    for conc in result.conclusions[:5]:
        print(f"  • {conc.get('derived_from')}: {conc.get('predicate')}({conc.get('args')}) "
              f"[conf: {conc.get('confidence', 0):.2f}]")
    
    # Test transitive reasoning
    print("\n--- Transitive Reasoning ---")
    engine2 = EnhancedEngine()
    engine2.add_fact('greater_than', [10, 5], confidence=1.0)
    engine2.add_fact('greater_than', [5, 2], confidence=1.0)
    result2 = engine2.infer(InferenceStrategy.FORWARD)
    
    print(f"Transitive conclusions: {len(result2.conclusions)}")
    for conc in result2.conclusions:
        if conc.get('derived_from') == 'transitive':
            print(f"  • {conc['args'][0]} > {conc['args'][1]} (conf: {conc['confidence']:.2f})")
    
    print("\nEngine stats:", engine.get_stats())
    print("=" * 60)


if __name__ == "__main__":
    test_enhanced_engine()
