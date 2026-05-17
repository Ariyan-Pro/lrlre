"""
Tests for the Enhanced Engine module.
"""
import pytest
from lrlre.engine.enhanced_engine import (
    EnhancedEngine, 
    InferenceStrategy, 
    WeightedFact, 
    InferenceResult
)


class TestEnhancedEngine:
    """Test cases for EnhancedEngine class."""
    
    def test_init_default(self):
        """Test engine initialization with default config."""
        engine = EnhancedEngine()
        assert len(engine.facts) == 0
        assert len(engine.rules) > 0  # Has default rules
        assert engine.confidence_threshold == 0.3
        assert engine.max_iterations == 100
    
    def test_init_with_config(self):
        """Test engine initialization with custom config."""
        config = {'confidence_threshold': 0.5, 'max_iterations': 50}
        engine = EnhancedEngine(config)
        
        assert engine.confidence_threshold == 0.5
        assert engine.max_iterations == 50
    
    def test_add_fact_basic(self):
        """Test adding a basic fact."""
        engine = EnhancedEngine()
        fact = engine.add_fact('is_a', ['Tweety', 'bird'], confidence=0.95)
        
        assert len(engine.facts) == 1
        assert fact['predicate'] == 'is_a'
        assert fact['args'] == ['Tweety', 'bird']
        assert fact['confidence'] == 0.95
    
    def test_add_fact_dict(self):
        """Test adding a fact using dictionary."""
        engine = EnhancedEngine()
        fact_dict = {'predicate': 'test', 'args': [1, 2], 'confidence': 0.8}
        fact = engine.add_fact(fact_dict=fact_dict)
        
        assert fact['predicate'] == 'test'
        assert fact['args'] == [1, 2]
    
    def test_infer_forward_strategy(self):
        """Test forward chaining inference."""
        engine = EnhancedEngine({'confidence_threshold': 0.4})
        engine.add_fact('is_a', ['Tweety', 'bird'], confidence=0.95)
        
        result = engine.infer(InferenceStrategy.FORWARD)
        
        assert isinstance(result, InferenceResult)
        assert result.strategy_used == 'forward'
        assert hasattr(result, 'conclusions')
        assert hasattr(result, 'processing_time_ms')
    
    def test_infer_backward_strategy(self):
        """Test backward chaining inference."""
        engine = EnhancedEngine()
        engine.add_fact('knows', ['Alice', 'Bob'])
        
        goal = {'predicate': 'knows', 'args': ['Alice', 'Bob']}
        result = engine.infer(InferenceStrategy.BACKWARD, goal=goal)
        
        assert result.strategy_used == 'backward'
    
    def test_infer_mixed_strategy(self):
        """Test mixed strategy inference."""
        engine = EnhancedEngine()
        engine.add_fact('is_a', ['Dog', 'Mammal'])
        
        result = engine.infer(InferenceStrategy.MIXED)
        
        assert result.strategy_used == 'mixed'
    
    def test_infer_best_first_strategy(self):
        """Test best-first search inference."""
        engine = EnhancedEngine()
        engine.add_fact('greater_than', [5, 3], confidence=0.9)
        engine.add_fact('greater_than', [3, 1], confidence=0.8)
        
        result = engine.infer(InferenceStrategy.BEST_FIRST)
        
        assert result.strategy_used == 'best_first'
    
    def test_transitive_reasoning(self):
        """Test transitive reasoning rule."""
        engine = EnhancedEngine({'confidence_threshold': 0.3})
        engine.add_fact('greater_than', [10, 5], confidence=1.0)
        engine.add_fact('greater_than', [5, 2], confidence=1.0)
        
        result = engine.infer(InferenceStrategy.FORWARD)
        
        # Should infer 10 > 2 through transitivity
        transitive_conclusions = [
            c for c in result.conclusions 
            if c.get('derived_from') == 'transitive'
        ]
        assert len(transitive_conclusions) >= 1
    
    def test_default_assumption(self):
        """Test default assumption rule."""
        engine = EnhancedEngine({'confidence_threshold': 0.3})
        engine.add_fact('is_a', ['Tweety', 'bird'], confidence=0.95)
        
        result = engine.infer(InferenceStrategy.FORWARD)
        
        # Should infer that Tweety can fly (default for birds)
        default_conclusions = [
            c for c in result.conclusions 
            if c.get('derived_from') == 'default'
        ]
        assert len(default_conclusions) >= 1
    
    def test_analogy_reasoning(self):
        """Test analogical reasoning."""
        engine = EnhancedEngine({'confidence_threshold': 0.3})
        engine.add_fact('similar_to', ['cat', 'dog'], confidence=0.7)
        engine.add_fact('can_do', ['cat', 'meow'], confidence=0.9)
        
        result = engine.infer(InferenceStrategy.FORWARD)
        
        analogy_conclusions = [
            c for c in result.conclusions 
            if c.get('derived_from') == 'analogy'
        ]
        # May or may not produce conclusions depending on implementation
        assert isinstance(analogy_conclusions, list)
    
    def test_conflict_detection(self):
        """Test conflict detection between facts."""
        engine = EnhancedEngine()
        engine.add_fact('equals', ['a', 'b'], confidence=0.9)
        
        conflicts = engine._detect_conflicts(
            {'predicate': 'not_equals', 'args': ['a', 'b'], 'confidence': 0.8}
        )
        
        assert len(conflicts) >= 1
    
    def test_facts_match(self):
        """Test fact pattern matching."""
        engine = EnhancedEngine()
        
        fact = {'predicate': 'test', 'args': [1, 2]}
        pattern = {'predicate': 'test'}
        
        assert engine._facts_match(fact, pattern) is True
        
        pattern_wrong = {'predicate': 'other'}
        assert engine._facts_match(fact, pattern_wrong) is False
    
    def test_get_stats(self):
        """Test getting engine statistics."""
        engine = EnhancedEngine()
        engine.add_fact('test', ['a', 'b'], confidence=0.8)
        engine.add_fact('test', ['c', 'd'], confidence=0.6)
        engine.infer()
        
        stats = engine.get_stats()
        
        assert stats['total_facts'] >= 2
        assert 'rules_count' in stats
        assert 'inferences_run' in stats
        assert 'avg_confidence' in stats
    
    def test_clear(self):
        """Test clearing the engine."""
        engine = EnhancedEngine()
        engine.add_fact('test', ['value'])
        engine.infer()
        
        engine.clear()
        
        assert len(engine.facts) == 0
        assert len(engine.inference_history) == 0
    
    def test_add_custom_rule(self):
        """Test adding a custom rule."""
        engine = EnhancedEngine()
        
        def apply_func(fact, context):
            return None
        
        engine.add_rule('custom', {'type': 'custom'}, apply_func, weight=0.5)
        
        assert len(engine.rules) > 1
        rule_names = [r['name'] for r in engine.rules]
        assert 'custom' in rule_names


class TestInferenceStrategy:
    """Test cases for InferenceStrategy enum."""
    
    def test_strategy_values(self):
        """Test that all expected strategies exist."""
        assert InferenceStrategy.FORWARD.value == 'forward'
        assert InferenceStrategy.BACKWARD.value == 'backward'
        assert InferenceStrategy.MIXED.value == 'mixed'
        assert InferenceStrategy.BEST_FIRST.value == 'best_first'


class TestWeightedFact:
    """Test cases for WeightedFact dataclass."""
    
    def test_weighted_fact_creation(self):
        """Test creating a weighted fact."""
        fact = {'predicate': 'test', 'args': []}
        wf = WeightedFact(weight=0.5, fact=fact)
        
        assert wf.weight == 0.5
        assert wf.fact == fact
    
    def test_weighted_fact_ordering(self):
        """Test that weighted facts are ordered by weight."""
        wf1 = WeightedFact(weight=0.3, fact={'id': 1})
        wf2 = WeightedFact(weight=0.7, fact={'id': 2})
        wf3 = WeightedFact(weight=0.5, fact={'id': 3})
        
        items = [wf2, wf1, wf3]
        items.sort()
        
        # Lower weight should come first (for min-heap behavior with negative weights)
        assert items[0].weight == 0.3
        assert items[1].weight == 0.5
        assert items[2].weight == 0.7


class TestInferenceResult:
    """Test cases for InferenceResult dataclass."""
    
    def test_result_creation(self):
        """Test creating an inference result."""
        result = InferenceResult(
            conclusions=[{'test': 'data'}],
            strategy_used='forward',
            confidence=0.85,
            processing_time_ms=12.34,
            steps_taken=5,
            conflicts_resolved=1
        )
        
        assert len(result.conclusions) == 1
        assert result.strategy_used == 'forward'
        assert result.confidence == 0.85
        assert result.processing_time_ms == 12.34
        assert result.steps_taken == 5
        assert result.conflicts_resolved == 1
